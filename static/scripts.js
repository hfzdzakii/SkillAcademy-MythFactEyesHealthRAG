document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("faktos")
    const spinner = document.getElementById("spinner")
    const hasil = document.getElementById("hasil")
    const konfiden = document.getElementById("konfiden")

    form.addEventListener("submit", async (event) => {
        event.preventDefault()
        const formData = new FormData(form)

        spinner.classList.remove("hidden")
        hasil.innerText = ""
        konfiden.innerText = ""

        try {
            const response = await fetch("/check_faktos", {
                method: "POST",
                body: formData,
            });
    
            const result = await response.json()
            console.log(result)
            hasil.innerText = `Hasil adalah ${result.kalimat}`
            konfiden.innerText = `Tingkat konfiden AI : ${result.konfiden}%`
        } catch (error) {
            hasil.innerText = "Ada kesalahan server. Coba lagi kembali."
        } finally {
            spinner.classList.add("hidden")
        }

    });
});