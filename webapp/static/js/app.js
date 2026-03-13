(function () {
  const form = document.getElementById('chat-form');
  const input = document.getElementById('message-input');
  const messagesEl = document.getElementById('chat-messages');
  const btnSend = document.getElementById('btn-send');
  const statusEl = document.getElementById('status-indicator');
  const paramFileInput = document.getElementById('param-file');
  const fileNameEl = document.getElementById('file-name');
  const uploadIntro = document.getElementById('upload-intro');
  const btnUpload = document.getElementById('btn-upload');

  function setStatus(text, active) {
    if (!statusEl) return;
    statusEl.textContent = text;
    statusEl.classList.toggle('active', !!active);
  }

  function addMessage(role, body) {
    const wrap = document.createElement('div');
    wrap.className = 'message ' + role;
    const label = role === 'user' ? 'OPERATOR' : 'AGENT';
    wrap.innerHTML =
      '<span class="msg-label">' + label + '</span>' +
      '<div class="msg-body"></div>';
    wrap.querySelector('.msg-body').textContent = body;
    messagesEl.appendChild(wrap);
    wrap.scrollIntoView({ behavior: 'smooth' });
  }

  async function sendToAgent(message) {
    addMessage('user', message);
    if (btnSend) btnSend.disabled = true;
    if (btnUpload) btnUpload.disabled = true;
    setStatus('— TRANSMITTING', true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message }),
      });
      const data = await res.json();

      if (!res.ok) {
        addMessage('agent', 'Error: ' + (data.error || res.statusText));
        setStatus('— ERROR', false);
        return;
      }

      addMessage('agent', data.reply || '(No response)');
      setStatus('— STANDBY', false);
    } catch (err) {
      addMessage('agent', 'Error: ' + (err.message || 'Network error'));
      setStatus('— ERROR', false);
    } finally {
      if (btnSend) btnSend.disabled = false;
      if (btnUpload) btnUpload.disabled = false;
    }
  }

  if (paramFileInput) {
    paramFileInput.addEventListener('change', function () {
      const file = this.files && this.files[0];
      fileNameEl.textContent = file ? file.name : 'No file chosen';
      btnUpload.disabled = !file;
    });
  }

  if (btnUpload && paramFileInput) {
    btnUpload.addEventListener('click', function () {
      const file = paramFileInput.files && paramFileInput.files[0];
      if (!file) return;

      const intro = (uploadIntro && uploadIntro.value.trim()) || '';
      const reader = new FileReader();
      reader.onload = function () {
        const content = typeof reader.result === 'string' ? reader.result : '';
        const message = intro
          ? intro + '\n\nParameter / mission file: ' + file.name + '\n\n```\n' + content + '\n```'
          : 'Parameter / mission file: ' + file.name + '\n\n```\n' + content + '\n```';
        sendToAgent(message);
        paramFileInput.value = '';
        fileNameEl.textContent = 'No file chosen';
        btnUpload.disabled = true;
      };
      reader.onerror = function () {
        addMessage('agent', 'Error: Could not read file.');
      };
      reader.readAsText(file, 'UTF-8');
    });
  }

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    const message = (input.value || '').trim();
    if (!message) return;

    input.value = '';
    sendToAgent(message);
  });
})();
