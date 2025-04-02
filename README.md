# Stock Management System GUI

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![Matplotlib](https://img.shields.io/badge/Charting-Matplotlib-orange.svg)

A comprehensive stock management system with graphical user interface built with Python and Tkinter, featuring data visualization with Matplotlib.

## Features

### Product Management
- ✅ Add new products with full details
- ✏️ Modify existing product information
- ❌ Delete products from inventory
- 🔍 Search products by reference or designation
- 📊 View availability statistics

### Advanced Functionality
- 📈 Interactive data visualization with Matplotlib
- 🔄 Multiple sorting options (by designation, price, or TVA)
- 💾 Save/Load inventory data to/from text files
- 📋 Filter products by availability status
- 🖱️ Right-click context menu for quick actions

### Data Visualization
- 📊 Bar charts for price and TVA distribution
- 🥧 Pie chart showing availability ratio
- Automatic chart updates on data changes

## Screenshots

![Main Interface](https://via.placeholder.com/800x500?text=Stock+Management+Main+Interface)
*Main application interface with product table*

![Statistics View](https://via.placeholder.com/800x500?text=Data+Visualization+Dashboard)
*Interactive data visualization dashboard*

## Installation

1. Clone the repository:
```bash
git clone https://github.com/An009/stockManager_gui_tkinter.git
 ```
Install required dependencies:
```bash
pip install -r requirements.txt
```
Or manually install:
```bash
pip install tkinter matplotlib
```
Run the application:
```bash
python gestion_de_stock_GUI_2.0.py
```
## Usage
Menu Options
File:

Save: Export current inventory to a text file

Open: Load inventory from a text file

Quit: Exit the application

## Tasks:

View Statistics: Show data visualization dashboard

View All Products: Display complete inventory

Filter by Availability: Show only available/unavailable products

Search: Find products by reference or designation

Add/Modify/Delete: Product management functions

Sort: Various sorting options for the product list

## Keyboard Shortcuts
Right-click on table rows for quick actions

Use scrollbar to navigate long product lists

## Code Structure
```bash
Stock Management System/
├── Product Class          - Core product data model
├── Stock Class            - Inventory management logic
├── GUI Class              - User interface implementation
│   ├── Main Window        - Primary application frame
│   ├── Product Table      - Data display component
│   ├── Search Panel       - Product lookup interface
│   ├── Form Panel         - Data entry forms
│   └── Statistics Panel   - Data visualization
└── Main Execution         - Application entry point
```
Technical Details
Core Classes
Produit (Product)

Stores product information:

Reference (unique identifier)

Designation (product name/description)

Unit price

VAT rate

Availability status

Stock (Inventory)

Manages collection of products

Provides search/sort/filter functionality

Handles file I/O operations

Gestion_Stock (GUI)

Implements all user interface components

Manages application state and user interactions

Integrates Matplotlib for data visualization

Requirements
Python 3.x

Tkinter (usually included with Python)

Matplotlib (pip install matplotlib)

License
this project is under BSD 2-Clause License-

#Contributions welcome! Please fork the repository and submit pull requests

