(function () {
  const form = document.getElementById('chat-form');
  const input = document.getElementById('message-input');
  const messagesEl = document.getElementById('chat-messages');
  const btnSend = document.getElementById('btn-send');
  const statusEl = document.getElementById('status-indicator');

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

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    const message = (input.value || '').trim();
    if (!message) return;

    addMessage('user', message);
    input.value = '';
    btnSend.disabled = true;
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
      btnSend.disabled = false;
    }
  });
})();
