document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("sidebar-toggle").addEventListener("click", toggleSidebar);
});

function toggleSidebar() {
    const sidebarLinks = document.getElementById('sidebar-links');
    sidebarLinks.classList.toggle('hidden');
}