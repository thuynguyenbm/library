// import fileSaver from "https://cdn.skypack.dev/file-saver@2.0.5";
// function exportCSV() {
//   let csv = [];
//   const rows = document.querySelectorAll("table tr");

//   for (const row of rows.values()) {
//     const cells = row.querySelectorAll("td, th");
//     const rowText = Array.from(cells).map((cell) => cell.innerText);
//     csv.push(rowText.join(","));
//   }
//   const csvFile = new Blob([csv.join("\n")], {
//     type: "text/csv;charset=utf-8;"
//   });
//   saveAs(csvFile, "data.csv");
// }

// document.querySelector("button").addEventListener("click", exportCSV);

function getFilteredData() {
  const selectElement = document.querySelector("#genre");
  console.log(selectElement)
  setTimeout(5000)
  const selectedGenre = selectElement.children[selectElement.selectedIndex].value;
  console.log(selectedGenre)
  if (selectedGenre) {
    url=`/filter?genre=${selectedGenre}`
    console.log(url)
    window.location.href = url; 
  }
}

function askStudentId(){
  let sId = prompt("Please enter the student id");
  if (sId != "") {
    url=`/return/${sId}`
    window.location.href = url
  }
  else window.location.href =  `/1`
}
