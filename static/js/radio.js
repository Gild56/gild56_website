document.addEventListener("DOMContentLoaded", function() {
    const audio = document.getElementById("radio")
    const cover = document.getElementById("cover")
    const titleEl = document.getElementById("title")
    const authorEl = document.getElementById("author")
    let currentFile = null

    document.getElementById("volume").addEventListener("input", (e)=>{
        audio.volume = e.target.value
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
            audio.src = "/" + data.file

            titleEl.innerText = data.title || data.file.split("/").pop()
            authorEl.innerText = data.author || "Unknown"

            cover.src = data.author
                ? "/static/radio/covers/" + data.author + ".jpg"
                : "/static/radio/covers/default.jpg"

            audio.addEventListener("loadedmetadata", function init() {
                const offset = Date.now()/1000 - data.start
                audio.currentTime = Math.max(offset, 0)
                audio.play().catch(()=>console.log("Autoplay blocked"))
                audio.removeEventListener("loadedmetadata", init)
            })

        } else {
            const offset = Date.now()/1000 - data.start
            if (Math.abs(audio.currentTime - offset) > 1) {
                audio.currentTime = offset
            }
        }
    }

    loadRadio()
    setInterval(loadRadio, 1000)
})
