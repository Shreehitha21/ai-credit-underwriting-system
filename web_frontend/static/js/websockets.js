// --- THIS IS THE CRUCIAL FIX FOR DEPLOYMENT ---
// We must use the live, secure URL of your Render backend.
// Replace this with the URL of your 'ai-credit-backend' service.
const URL = 'wss://ai-credit-backend.onrender.com';

let socket;

function connectWebSocket() {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user) return;

    if (socket) socket.disconnect();

    // Connect to the live WebSocket server, passing the user's ID for authentication.
    socket = io(URL, {
        path: "/socket.io/", // Ensure the path is correct
        auth: { userId: user.id }
    });

    socket.on('connect', () => {
        showNotification('Connected to real-time server.');
    });

    socket.on('notification', (data) => {
        showNotification(data.message);
        
        // If the notification includes a report URL, refresh the application list
        if (data.report_url) {
            if (window.location.pathname.includes('customer.html')) {
                loadUserApplications();
            }
        }
        // If the admin dashboard is open, refresh its list too
        if (window.location.pathname.includes('admin.html')) {
            loadAdminApplications();
        }
    });

    socket.on('disconnect', () => {
        showNotification('Disconnected from real-time server.', true);
    });

    socket.on('connect_error', (err) => {
        console.error('WebSocket connection error:', err.message);
        showNotification('Real-time connection failed. Refreshing the page might help.', true);
    });
}

function showNotification(message, isError = false) {
    const notificationsContainer = document.getElementById('notifications');
    if (!notificationsContainer) return;

    const notification = document.createElement('div');
    notification.className = `notification ${isError ? 'error' : ''}`;
    notification.textContent = message;
    notificationsContainer.appendChild(notification);

    speakText(message, navigator.language);

    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Connect on page load if it's a page that needs real-time updates
if (window.location.pathname.includes('customer.html') || window.location.pathname.includes('admin.html')) {
    connectWebSocket();
}
