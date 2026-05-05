document.addEventListener('DOMContentLoaded', () => {
    const urlInput = document.getElementById('urlInput');
    const fetchBtn = document.getElementById('fetchBtn');
    const loader = document.getElementById('loader');
    const btnText = fetchBtn.querySelector('.btn-text');
    const errorMsg = document.getElementById('errorMsg');
    const resultSection = document.getElementById('resultSection');
    
    // Video Info Elements
    const videoThumb = document.getElementById('videoThumb');
    const videoTitle = document.getElementById('videoTitle');
    const videoAuthor = document.getElementById('videoAuthor');
    const videoDuration = document.getElementById('videoDuration');
    const streamsList = document.getElementById('streamsList');

    const API_URL = '/api/info';

    fetchBtn.addEventListener('click', async () => {
        const url = urlInput.value.trim();
        
        if (!url) {
            showError('Por favor, insira uma URL válida do YouTube.');
            return;
        }

        if (!url.includes('youtube.com/') && !url.includes('youtu.be/')) {
            showError('A URL deve ser do YouTube.');
            return;
        }

        startLoading();
        
        try {
            const response = await fetch(`${API_URL}?url=${encodeURIComponent(url)}`);
            const data = await response.json();

            if (data.error) {
                showError(data.error);
            } else {
                displayResult(data);
            }
        } catch (err) {
            showError('Ocorreu um erro ao conectar com o servidor. Tente novamente mais tarde.');
            console.error(err);
        } finally {
            stopLoading();
        }
    });

    function displayResult(data) {
        errorMsg.textContent = '';
        resultSection.classList.remove('hidden');
        
        videoThumb.src = data.thumbnail;
        videoTitle.textContent = data.title;
        videoAuthor.textContent = data.author;
        videoDuration.textContent = formatDuration(data.duration);
        
        streamsList.innerHTML = '';
        
        data.streams.forEach(stream => {
            const item = document.createElement('a');
            item.className = 'stream-item';
            item.href = stream.url;
            item.setAttribute('download', `${data.title}.mp4`);
            item.target = '_blank';
            
            item.innerHTML = `
                <div class="stream-info">
                    <span class="res-tag">${stream.resolution}</span>
                    <span class="mime-type">MP4</span>
                </div>
                <div class="stream-size">
                    <strong>${stream.size} MB</strong>
                </div>
            `;
            
            streamsList.appendChild(item);
        });

        // Scroll to result
        resultSection.scrollIntoView({ behavior: 'smooth' });
    }

    function formatDuration(seconds) {
        const h = Math.floor(seconds / 3600);
        const m = Math.floor((seconds % 3600) / 60);
        const s = seconds % 60;
        
        if (h > 0) {
            return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
        }
        return `${m}:${s.toString().padStart(2, '0')}`;
    }

    function showError(msg) {
        errorMsg.textContent = msg;
        resultSection.classList.add('hidden');
    }

    function startLoading() {
        fetchBtn.disabled = true;
        loader.style.display = 'block';
        btnText.style.display = 'none';
        errorMsg.textContent = '';
    }

    function stopLoading() {
        fetchBtn.disabled = false;
        loader.style.display = 'none';
        btnText.style.display = 'block';
    }
});
