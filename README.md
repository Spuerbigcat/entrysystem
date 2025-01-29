### **NFC Entry Management System**
## **Overview**
This system is a Python script that manages university, junior college, and graduate school entry and exit using NFC technology.
By tapping a student ID card on an NFC reader, the system logs entry and exit records into a Google Spreadsheet.
Additionally, it has an automatic reset function that clears entry statuses at specified times.

## **Features**
- Reads student ID cards using an NFC reader
- Identifies department information from student ID numbers
- Logs entry and exit times
- Records data in a Google Spreadsheet
- Automatically resets entry statuses at 9:20 AM and 9:20 PM
- Provides audio notifications for entry and exit

---

## **Requirements**
### **Required Hardware**
- NFC Reader (e.g., PaSoRi)

### **Environment**
- Python 3.x
- Windows or Linux

---

## **Setup Instructions**
### **1. Google Spreadsheet Configuration**
1. Create a service account on Google Cloud Console and download the `JSON key`.
2. Create a Google Spreadsheet and obtain the sheet ID.
3. Place the `JSON key` file in the project directory.
4. Enable `Google Sheets API`.

---

## **How to Run**
1. Connect the NFC reader to your PC.
2. Run the script:

```bash
python entrysystem.py
```

---

## **Project Structure**
```
/entrysystem/
│── entrysystem.py   # Main script
│── README.md        # This document
```

---

## **Process Flow**
1. Detect an NFC tag
2. Retrieve the student ID and determine department information
3. Manage entry and exit statuses
4. Record logs in a Google Spreadsheet
5. Execute reset process at specified intervals

---

## **Troubleshooting**
| **Error** | **Cause** | **Solution** |
|-----------|----------|-------------|
| `Failed to initialize Google Sheets API` | Incorrect API key settings | Verify the JSON file path and spreadsheet ID |
| `NFC Read Error` | NFC reader not recognized | Check USB connection and reinstall drivers |
| `Data not recorded in the spreadsheet` | Incorrect sheet name | Ensure the sheet is named "MORI" |

---

## **License**
This project is released under the MIT License.

---

## **Author**
- **Name**: [Superbigcat]


