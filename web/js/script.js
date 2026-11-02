// SCHNAPS-BIER-SIRUP
function handleKeyPressSBS(event) {
    let inpAge = document.getElementById("inputAge")
    let drink = document.getElementById('spanDrink')
 
    let age = inpAge.value
 
    if (age >= 18) {
        drink.textContent = "Schnaps!"
    } else if (age >= 16) {
        drink.textContent = "Bier!"
    } else {
        drink.textContent = "Sirup!"
    }
}
 
// CLICKER
let count = 0
 
function handleBtnClicker(event) {
    count += 1
    let spanClick = document.getElementById("spanClicker")
    spanClick.textContent = count
}
 
let funCount = 0
const funProb = 0.1
 
function handleBtnFunClicker(event) {
    funCount = funCount + 1
    const randFloat = Math.random()
    if(randFloat < funProb){
        funCount = 0
    }
    spanFunClicker.textContent = funCount
}
 
// DICE
const l = 200
const diceImages = [
    [[0.5*l, 0.5*l]],
    [[0.25*l, 0.25*l],[0.75*l, 0.75*l]],
    [[0.25*l, 0.25*l],[0.5*l, 0.5*l],[0.75*l, 0.75*l]],
    [[0.25*l, 0.25*l],[0.75*l, 0.75*l],[0.75*l, 0.25*l],[0.25*l, 0.75*l]],
    [[0.25*l, 0.25*l],[0.75*l, 0.75*l],[0.75*l, 0.25*l],[0.25*l, 0.75*l],[0.5*l, 0.5*l]],
    [[0.25*l, 0.25*l],[0.25*l, 0.5*l],[0.25*l, 0.75*l],[0.75*l, 0.25*l],[0.75*l, 0.5*l],[0.75*l, 0.75*l]],
]
 
function handleBtnDice(event) {
    let randomInt = Math.floor(Math.random() * 6) + 1
    spanDice.textContent = randomInt
 
    // draw dice
    const ctx = canvasDice.getContext('2d')
    canvasDice.width = l
    canvasDice.height = l
 
    ctx.clearRect(0, 0, canvasDice.width, canvasDice.height) // Clear the canvas
 
    // Draw the dice outline
    ctx.strokeStyle = 'black'
    // ctx.lineWidth = 5
    const diceImage = diceImages[randomInt-1]
    diceImage.forEach(point => {
        ctx.beginPath()
        ctx.arc(point[0],point[1], 20, 0, 2 * Math.PI)
        ctx.fill()
        ctx.stroke() // Outline the circle
        ctx.closePath()
    })
}
 
// CHAR COUNTER
function handleInputTextArea(event) {
    let txtArea = document.getElementById("txtArea")
    let spanBuchstaben = document.getElementById("spanBuchstabenCounter")
    spanBuchstaben.textContent = txtArea.value.length
}
 
// DATE
function handleDateSelected(event) {
    const inpDate = document.getElementById('inputDate')
    const dateSelected = inpDate.value
 
    // get date of today
    const today = new Date()
    const year = today.getFullYear()  // Get the current year (e.g., 2023)
    const month = today.getMonth() + 1  // Get the current month (January is 0)
    const day = today.getDate()  // Get the current day of the month
 
    // Format the date (e.g., YYYY-MM-DD)
    const dateToday = `${year}-${month < 10 ? '0' + month : month}-${day < 10 ? '0' + day : day}`
 
    // create date objects
    const start = new Date(dateSelected)
    const end = new Date(dateToday)
 
    // determine difference
    const deltaMs = end - start
    const deltaDays = Math.floor(deltaMs / (1000 * 60 * 60 * 24))
 
    const passedDays = document.getElementById('spanPassedDays')
    passedDays.textContent = deltaDays
}