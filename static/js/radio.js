document.addEventListener("DOMContentLoaded", function() {
const audio = document.getElementById("radio")
const cover = document.getElementById("cover")
const titleEl = document.getElementById("title")
const authorEl = document.getElementById("author")
const volumeSlider = document.getElementById("volume")

let currentFile = null

const savedVolume = localStorage.getItem("radioVolume")

if (savedVolume !== null) {
    volumeSlider.value = savedVolume

    const v = parseFloat(savedVolume)
    audio.volume = v === 0 ? 0 : Math.exp((v - 1) * 5)
} else {
    audio.volume = 1
}

volumeSlider.addEventListener("input", (e) => {
    const v = parseFloat(e.target.value)

    audio.volume = v === 0
        ? 0
        : Math.exp((v - 1) * 5)

    localStorage.setItem("radioVolume", v)
})

async function loadRadio() {
    const res = await fetch("/radio/now")
    const data = await res.json()

    if (data.error) return

    if (data.file === null) {
        audio.pause()
        currentFile = null
        return
    }

    if (currentFile !== data.file) {
        currentFile = data.file

        audio.src = data.file

        titleEl.innerText =
            data.title || data.file.split("/").pop()

        authorEl.innerText =
            data.author || "Unknown"

        cover.src = data.author
            ? `https://raw.githubusercontent.com/Gild56/gild56_website_lists/refs/heads/main/images/covers/${encodeURIComponent(data.author)}.png`
            : "https://raw.githubusercontent.com/Gild56/gild56_website_lists/refs/heads/main/images/covers/default.png"

        audio.addEventListener("loadedmetadata", function init() {
            const offset = Date.now() / 1000 - data.start

            audio.currentTime = Math.max(offset, 0)

            audio.play().catch(() =>
                console.log("Autoplay blocked")
            )

            audio.removeEventListener("loadedmetadata", init)
        })
    } else {
        const offset = Date.now() / 1000 - data.start

        if (Math.abs(audio.currentTime - offset) > 1) {
            audio.currentTime = offset
        }
    }
}

loadRadio()
setInterval(loadRadio, 1000)
})
