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
            const response = await fetch("/predict", {
                method: "POST",
                body: formData,
            });
    
            const result = await response.json()
            console.log(result)
            hasil.innerText = `${result.result}`
            konfiden.innerText = `AI confidence level : ${result.confidence}%`
        } catch (error) {
            hasil.innerText = "Server error, please try again later."
        } finally {
            spinner.classList.add("hidden")
        }

    });
});