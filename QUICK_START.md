# Quick Start Guide - New Features

## 🎯 Quick Access to New Features

### 1. **Hover Over Tenant Names to See Quick Profile** 
- Go to `/tenants/` (Tenants menu)
- Hover your mouse over any tenant name
- A popup appears with:
  - Personal info
  - Financial status
  - Last 5 payments
  - Quick action buttons

### 2. **View Complete Transaction History**
- Click on any tenant name or "View Details" button
- Go to `/tenants/<id>/` 
- Click the "Transaction History" tab
- See every payment, deposit update, and account change
- Each entry shows: Date, Type, Amount, Previous Balance, New Balance, Description

### 3. **Record Payment (Updated Form)**
- Go to `/payments/add/` or use "Record Payment" button
- Form now includes optional:
  - Tenant selection
  - Amount paid
  - Months covered
  - Payment notes
  - Security deposit (if updating)
  - Initial balance (if needed)
- Submit to record and automatically log transaction

### 4. **Delete Tenant (Choose Your Option)**
- Go to any tenant's profile
- Click "Delete Tenant" button
- Choose between:
  - **Soft Delete (Recommended)**: Keep all history, mark inactive
  - **Hard Delete (Caution)**: Permanently remove everything
- Confirm your choice

### 5. **View Dashboard KPIs**
- Go to `/` (Dashboard)
- See all key metrics:
  - Total Tenants
  - Occupied/Vacant Houses
  - Overdue Tenants
  - Monthly Collection
  - Outstanding Rent
- Scroll down to see "House Status & Rent Collection" table

### 6. **Check Overdue Tenants**
- Click "Overdue Tenants" card on dashboard
- Or go to `/overdue/`
- See all tenants with overdue payments
- Shows: Name, House, Days Overdue, Balance, Payment Status

### 7. **Access from Mobile or Another Device**
1. Find the IP address of your computer (in Windows: `ipconfig` in cmd)
2. On mobile/other device browser, go to: `http://<computer-ip>:8000`
3. Example: `http://192.168.1.100:8000`
4. Interface automatically adjusts for mobile screen
5. Sidebar becomes collapsible menu

---

## 📊 Dashboard Breakdown

**Top Row Cards:**
- Total Tenants: Number of active tenants
- Occupied Houses: Houses with tenants
- Vacant Houses: Available properties  
- Overdue Tenants: Click to view details

**Financial Section:**
- This Month's Collections: Total payments received this month
- Total Outstanding: Sum of all tenant balances

**House Table:**
Shows each house with:
- Status (Occupied/Vacant)
- Tenant Name
- Monthly Rent
- Outstanding Balance
- Payment Status (Overdue/Pending/Paid)

---

## ⚙️ Running the System

### Start the Server
```bash
cd "c:\Users\DELL\Desktop\Apartment Management System"
python manage.py runserver
```

### Access Locally
- `http://localhost:8000` (same computer)
- `http://127.0.0.1:8000` (same computer)

### Access from Mobile/Other Devices
- Replace `localhost` with your computer's IP address
- Example: `http://192.168.1.100:8000`

### Find Your IP Address
- Windows: Open Command Prompt and type `ipconfig`, look for "IPv4 Address"
- Mac/Linux: Open Terminal and type `ifconfig`

---

## 💡 Tips & Best Practices

1. **Use Soft Delete First**: If you need to remove a tenant, use soft delete to keep history
2. **Check Transaction History**: Always verify transaction records are logged correctly
3. **Mobile Access**: Test system on mobile to ensure accessibility for parents
4. **House Rent**: Make sure each house has correct monthly_rent set in admin
5. **Backups**: Regularly backup your `db.sqlite3` file
6. **Security**: Change SECRET_KEY in settings.py if deploying publicly

---

## 🔒 Data Safety

- All transactions are logged automatically
- Soft deleted tenants keep all history
- Hard delete requires confirmation (use cautiously)
- Transaction history is immutable (cannot be changed after creation)
- Regular database backups recommended

---

## 📱 Mobile Features

The system is fully responsive on:
- ✅ iPhones & iPads
- ✅ Android phones & tablets
- ✅ Any modern browser

All features work the same on mobile:
- Hover popups become tap-to-view
- Tables adapt to screen size
- Navigation menu collapses on small screens
- Forms are touch-optimized

---

## 🆘 Troubleshooting

### "Cannot connect from mobile"
- Check if computer is on same WiFi
- Verify you're using correct IP address (from `ipconfig`)
- Check firewall isn't blocking port 8000
- Try: `python manage.py runserver 0.0.0.0:8000`

### "Transaction not showing in history"
- Refresh the page
- Transaction logging is automatic on payments
- Check transaction history tab in tenant profile

### "Soft delete didn't work"
- Tenant marked as inactive but data preserved
- To permanently delete, use hard delete option

---

## 📞 Support

Refer to FEATURES_IMPLEMENTED.md for detailed technical documentation.
