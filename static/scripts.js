document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("faktos")
    const spinner = document.getElementById("spinner")
    const hasil = document.getElementById("hasil")
    
    form.addEventListener("submit", async (event) => {
        event.preventDefault()
        const formData = new FormData(form)

        spinner.classList.remove("hidden")
        hasil.innerHTML = ""

        try {
            const response = await fetch("/predict", {
                method: "POST",
                body: formData,
            });
    
            const result = await response.json()
            console.log(result)
            const tempDiv = document.createElement('div')
            tempDiv.innerHTML = result.result
            const processedText = tempDiv.textContent.replace(/\n/g, '<br>')
            hasil.innerHTML = processedText
        } catch (error) {
            hasil.innerHTML = "Server error, please try again later."
        } finally {
            spinner.classList.add("hidden")
        }

    });
});