document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("faktos")
    const spinner = document.getElementById("spinner")
    const hasil = document.getElementById("hasil")

    form.addEventListener("submit", async (event) => {
        event.preventDefault()
        const formData = new FormData(form)

        spinner.classList.remove("hidden")
        hasil.innerText = ""
        
        try {
            const response = await fetch("/check_faktos", {
                method: "POST",
                body: formData,
            });
    
            const result = await response.json()
            hasil.innerText = `Hasil adalah ${result.kalimat}`
        } catch (error) {
            hasil.innerText = "Ada kesalahan server. Coba lagi kembali."
        } finally {
            spinner.classList.add("hidden")
        }

    });
});