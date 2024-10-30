function getMitigation(threat, totalScore) {
    let mitigation;
  
    if (threat === "Tampering") {
      if (totalScore >= 30) {
        mitigation = "Implement encryption and logging to detect and prevent tampering.";
      } else if (totalScore >= 20) {
        mitigation = "Regularly monitor and update access control mechanisms.";
      } else {
        mitigation = "Use checksum or hash functions to verify data integrity periodically.";
      }
    } else if (threat === "Information Disclosure") {
      if (totalScore >= 30) {
        mitigation = "Use strong encryption and implement access controls to protect sensitive information.";
      } else if (totalScore >= 20) {
        mitigation = "Restrict access to sensitive data and log access requests.";
      } else {
        mitigation = "Ensure data is not exposed by default and limit access as needed.";
      }
    } else if (threat === "Spoofing") {
      if (totalScore >= 30) {
        mitigation = "Implement multi-factor authentication and strict identity validation.";
      } else if (totalScore >= 20) {
        mitigation = "Use secure channels and certificate-based authentication.";
      } else {
        mitigation = "Regularly update passwords and use anti-spoofing measures.";
      }
    } else if (threat === "Elevation of Privilege") {
      if (totalScore >= 30) {
        mitigation = "Limit privileged access, implement least privilege principle, and monitor privilege escalations.";
      } else if (totalScore >= 20) {
        mitigation = "Regularly review and update privilege settings.";
      } else {
        mitigation = "Educate users on privilege policies and review permissions periodically.";
      }
    } else {
      mitigation = "General mitigation: Review system settings and monitor access controls.";
    }
  
    return mitigation;
  }
  
  function addThreat() {
    const asset = document.getElementById("asset").value;
    const threat = document.getElementById("threat").value;
    const damage = parseInt(document.getElementById("damage").value) || 0;
    const reproducibility = parseInt(document.getElementById("reproducibility").value) || 0;
    const exploitability = parseInt(document.getElementById("exploitability").value) || 0;
    const affected = parseInt(document.getElementById("affected").value) || 0;
    const discoverability = parseInt(document.getElementById("discoverability").value) || 0;
    
    const totalScore = damage + reproducibility + exploitability + affected + discoverability;
  
    let priority;
    let priorityColor;
  
    if (totalScore >= 30) {
      priority = "Tinggi";
      priorityColor = "high-priority"; // Merah
    } else if (totalScore >= 20) {
      priority = "Sedang";
      priorityColor = "medium-priority"; // Kuning
    } else {
      priority = "Rendah";
      priorityColor = "low-priority"; // Hijau
    }
  
    // Dapatkan langkah mitigasi berdasarkan jenis ancaman dan skor total
    const mitigation = getMitigation(threat, totalScore);
  
    // Tambahkan baris ke tabel
    const tableBody = document.getElementById("threatTable").getElementsByTagName("tbody")[0];
    const newRow = tableBody.insertRow();
  
    newRow.innerHTML = `
      <td>${asset}</td>
      <td>${threat}</td>
      <td>${damage}</td>
      <td>${reproducibility}</td>
      <td>${exploitability}</td>
      <td>${affected}</td>
      <td>${discoverability}</td>
      <td>${totalScore}</td>
      <td class="${priorityColor}">${priority}</td>
      <td>${mitigation}</td>
    `;
  
    // Reset form setelah data ditambahkan
    document.getElementById("damage").value = "";
    document.getElementById("reproducibility").value = "";
    document.getElementById("exploitability").value = "";
    document.getElementById("affected").value = "";
    document.getElementById("discoverability").value = "";
  }
  