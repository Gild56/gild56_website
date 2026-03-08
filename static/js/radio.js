document.addEventListener("DOMContentLoaded", function(){

    const audio = document.getElementById("radio")
    const cover = document.getElementById("cover")
    const titleEl = document.getElementById("title")
    const authorEl = document.getElementById("author")
    let currentFile = null
    let initialized = false

    document.getElementById("volume").addEventListener("input", (e)=>{
        audio.volume = e.target.value
    })

    async function loadRadio() {
        const res = await fetch("/radio/now")
        const data = await res.json()
        if (data.error) return

        // Si c'est le même morceau, ne rien faire
        if (currentFile === data.file) return
        currentFile = data.file

        audio.src = "/" + data.file

        // mettre à jour le titre et auteur
        titleEl.innerText = data.title || data.file.split("/").pop()
        authorEl.innerText = data.author || "Unknown"
        cover.src = data.author
            ? "/static/radio/covers/" + data.author + ".jpg"
            : "/static/radio/covers/default.jpg"

        // On n'ajuste currentTime qu'une seule fois par morceau
        audio.oncanplay = () => {
            if (!initialized) {
                const offset = Date.now()/1000 - data.start
                audio.currentTime = Math.max(offset, 0)
                audio.play().catch(()=>console.log("Autoplay blocked"))
                initialized = true
            }
        }
    }

    loadRadio()
    setInterval(loadRadio, 20000)

    function checkHourFade() {
        const now = new Date()
        if (now.getMinutes() == 59 && now.getSeconds() > 50) {
            let vol = audio.volume
            const fade = setInterval(()=>{
                vol -= 0.05
                audio.volume = Math.max(vol,0)
                if(vol <= 0) clearInterval(fade)
            }, 200)
        }
    }
    setInterval(checkHourFade, 1000)

    // Réinitialiser flag quand le morceau change
    audio.addEventListener("ended", ()=>{ initialized = false })
})