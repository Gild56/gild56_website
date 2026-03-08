
(function() {
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme) {
        document.documentElement.classList.toggle("dark-mode", savedTheme === "dark");
    } else {
        const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
        document.documentElement.classList.toggle("dark-mode", prefersDark);
    }
})();

function toggleDarkMode() {
    document.documentElement.classList.add("no-transition");

    const isDark = document.documentElement.classList.toggle("dark-mode");
    localStorage.setItem("theme", isDark ? "dark" : "light");

    setTimeout(() => {
        document.documentElement.classList.remove("no-transition");
    }, 0);
}
