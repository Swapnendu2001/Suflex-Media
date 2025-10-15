(function(){
  const toastHost = document.getElementById('toast');
  const loadingOverlay = document.getElementById('loadingOverlay');
  const cards = document.querySelectorAll('.card');

  function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) === ' ') c = c.substring(1, c.length);
      if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
  }

  function deleteCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`;
  }

  function showLoading(show) {
    if (loadingOverlay) {
      if (show) {
        loadingOverlay.classList.remove('hidden');
      } else {
        loadingOverlay.classList.add('hidden');
      }
    }
  }

  async function verifyAuth() {
    const hashedEmail = getCookie('hashed_email');
    const hashedPassword = getCookie('hashed_password');
    
    if (!hashedEmail || !hashedPassword) {
      console.log("No credentials found, redirecting to login...");
      toast("Please login to continue", "error");
      setTimeout(() => {
        window.location.href = "/login";
      }, 1000);
      return false;
    }

    try {
      console.log("Verifying stored credentials...");
      const res = await fetch("/api/auto-login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify({
          hashed_email: hashedEmail,
          hashed_password: hashedPassword
        }),
        credentials: 'include'
      });

      if (!res.ok) {
        console.log("Authentication failed, clearing credentials...");
        deleteCookie('hashed_email');
        deleteCookie('hashed_password');
        toast("Authentication failed. Redirecting to login...", "error");
        setTimeout(() => {
          window.location.href = "/login";
        }, 1000);
        return false;
      }

      const data = await res.json().catch(() => null);
      if (data && data.status === "success") {
        console.log("✓ Authentication successful");
        showLoading(false);
        return true;
      } else {
        console.log("Invalid response, clearing credentials...");
        deleteCookie('hashed_email');
        deleteCookie('hashed_password');
        toast("Authentication failed. Redirecting to login...", "error");
        setTimeout(() => {
          window.location.href = "/login";
        }, 1000);
        return false;
      }
    } catch (err) {
      console.error("Error during authentication:", err);
      toast("Authentication error. Redirecting to login...", "error");
      setTimeout(() => {
        window.location.href = "/login";
      }, 1000);
      return false;
    }
  }

  (function initAuth() {
    showLoading(true);
    verifyAuth();
  })();

  cards.forEach(card => {
    card.addEventListener('click', function() {
      const page = this.dataset.page;
      handleCardClick(page);
    });

    card.addEventListener('mouseenter', function() {
      this.style.transition = 'all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1)';
    });
  });

  function handleCardClick(page) {
    const pageMap = {
      'analytics': {
        title: 'Analytics',
        url: '/admin/analytics'
      },
      'blogs': {
        title: 'Blogs',
        url: '/admin/blogs'
      },
      'admin-users': {
        title: 'Admin Users',
        url: '/admin/users'
      }
    };

    const pageInfo = pageMap[page];
    if (pageInfo) {
      toast(`Navigating to ${pageInfo.title}...`);
      setTimeout(() => {
        window.location.href = pageInfo.url;
      }, 800);
    }
  }

  function toast(message, type) {
    const host = toastHost || document.getElementById('toast');
    if (!host) return;
    
    const el = document.createElement('div');
    el.className = 'msg' + (type === 'error' ? ' error' : '');
    el.textContent = message;
    host.appendChild(el);
    
    setTimeout(() => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(6px)';
    }, 2200);
    
    setTimeout(() => {
      if (el.parentNode) host.removeChild(el);
    }, 2700);
  }

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      const toastMessages = toastHost.querySelectorAll('.msg');
      toastMessages.forEach(msg => {
        msg.style.opacity = '0';
        msg.style.transform = 'translateY(6px)';
        setTimeout(() => {
          if (msg.parentNode) toastHost.removeChild(msg);
        }, 300);
      });
    }
  });

})();