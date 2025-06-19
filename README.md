# Modern Expense Tracker

Ek user-friendly desktop application jo Python aur Tkinter ka use karke personal kharche track karta hai. Yeh application aapko aasani se apne kharchon ko log karne, dekhne, manage karne aur analyze karne mein madad karta hai.

## Features

* **Intuitive GUI:** Ek saaf, tabbed interface (`Add New Expense`, `View & Manage`, `Analytics & Reports`) jo Tkinter aur `ttk` (modern UI ke liye) se bana hai.
* **Persistent Data Storage:** Aapke sabhi kharche `expenses.csv` file mein save hote hain, jisse aapka data application band karne ke baad bhi surakshit rehta hai.
* **Unique Expense IDs:** Har kharche ko ek unique ID di jaati hai, jisse editing aur deletion bahut aasan aur reliable ho jaati hai.
* **Monthly Summary:** Kisi bhi mahine aur saal ke liye apne kul kharche turant dekhein.
* **Data Management:** Ek saaf table view se existing kharche ko aasani se edit ya delete karein.
* **Excel Export:** Apne sabhi kharche data ko professional `.xlsx` (Excel) spreadsheet mein export karein, aage ke analysis ya record-keeping ke liye.
* **Monthly Trend Graph:** Matplotlib ka upyog karke ek interactive bar chart ke saath samay ke saath apne kharchon ke patterns ko visualize karein.

## Technologies Used

* Python 3.x
* Tkinter (Python ki built-in GUI library)
* `tkinter.ttk` (Modern look ke liye themed Tkinter widgets)
* `csv` (CSV file operations ke liye)
* `datetime` (Date handling ke liye)
* `uuid` (Unique ID generate karne ke liye)
* `pandas` (Data manipulation aur Excel export ke liye)
* `matplotlib` (Graphs banane ke liye)

## How to Run the Application (Application kaise chalayein)

1.  **Prerequisites (Zaroori Cheezein):**
    * Apne system par Python 3.x install hona chahiye.
    * Ensure karein ki `pip` aapke system ke PATH mein configure kiya gaya hai.

2.  **Clone the Repository (Ya Download Karein):**
    Apne terminal ya PowerShell mein, jahan aap project ko save karna chahte hain, ye command run karein:
    ```bash
    git clone [https://github.com/YOUR_GITHUB_USERNAME/Python-Expense-Tracker.git](https://github.com/YOUR_GITHUB_USERNAME/Python-Expense-Tracker.git)
    cd Python-Expense-Tracker
    ```
    (Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username).

3.  **Install Dependencies (Zaroori Libraries Install Karein):**
    Project folder mein terminal ya PowerShell kholkar ye command run karein:
    ```bash
    pip install pandas openpyxl matplotlib
    ```
    Agar `pip` recognize nahi ho, toh ye try karein:
    ```bash
    python -m pip install pandas openpyxl matplotlib
    ```

4.  **Run the Application (Application Chalayein):**
    ```bash
    python app.py
    ```

## Project Structure

* `app.py`: Main application file jismein GUI logic aur expense management functions hain.
* `expenses.csv`: (Optional, pehli baar chalane par banta hai) Aapka expense data store karta hai. Ye file aam taur par Git dwara ignore ki jaati hai taaki personal data upload na ho.
* `.gitignore`: Git ko batata hai ki kin files aur directories ko ignore karna hai (jaise `__pycache__`, `venv`, `build/`, `dist/`).
* `README.md`: Yeh file, jo project ki jaankari deti hai.

## Future Enhancements (Bhavishya ke Sudhaar)

* Category ya date range ke hisab se kharche filter aur search karna.
* Alag-alag expense categories add karna.
* Budgeting features.
* Aur advanced reports (jaise categories ke liye pie charts).
* Multiple users ke liye user authentication.

---
**Note:** Yeh application desktop use ke liye design ki gayi hai (Windows, macOS, Linux). Ise सीधे mobile phones par nahi chalaya ja sakta kyunki `.exe` files Android ya iOS ke saath compatible nahi hoti hain. Mobile solutions ke liye, dedicated mobile development frameworks ya web applications ki zaroorat padegi.