let newNoteBtn = document.getElementById("newNoteBtn")
let messageFlash = document.getElementById("messageFlash")
function openNote(){
// dialog.showModal()
    let formText = `
            <dialog class="dialog position-fixed top-50 start-50 bg-body-secondary p-5 rounded-5 translate-middle" dialogBox>
                <form action='/createFile' class="formBox" method='post' >
                    <div class="mb-3">
                        <label for="fileName" class="form-label">File Name</label>
                        <input type="text" name='fileName' class="form-control" id="fileName" >
                    </div>
                    <button type="submit" id='submitNewFileBtn'  class="btn btn-primary">Create</button>
                    <button type="button" class="btn btn-danger" id="closeDialog">Close</button>
                </form>
            </dialog>
    `
    let boxDialog = document.createElement("div")
    boxDialog.innerHTML=formText
    document.body.append(boxDialog)
    let dialog = document.querySelector("dialog")
        dialog.showModal()
    let closeDialog = document.getElementById("closeDialog")
    closeDialog.addEventListener("click", function(){
        dialog.close()
        dialog.parentElement.remove()
    })

    let submitNewFileBtn = document.getElementById("submitNewFileBtn")

    submitNewFileBtn.addEventListener("click", function(event){
        // event.preventDefault()

    })

}
newNoteBtn.addEventListener("click", function(){
    openNote()
})

if (messageFlash){
     setTimeout(function(){
        messageFlash.style.left="0%"
    }, 300)
      setTimeout(function(){
        messageFlash.style.left="-100%"
    }, 4500)
    setTimeout(function(){
        messageFlash.remove()
    }, 6000)

    
}



