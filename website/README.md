# Campaign Pro Marketing Website

This is the marketing website for the Campaign Pro election campaign management system.

## Files Structure

- `index.html` - Home/Landing page with hero section and feature overview
- `features.html` - Detailed explanation of all features and how they work
- `pricing.html` - Pricing plans and feature comparison
- `about.html` - About the system and company mission
- `contact.html` - Contact form and information
- `styles.css` - Website styles using the same theme as the application
- `script.js` - JavaScript for interactivity (navbar scroll, form handling, animations)

## How to Use

### Option 1: Using Python (Recommended)

1. Navigate to the website folder:
```bash
cd website
```

2. Run the server:
```bash
python -m http.server 8000
```

3. Open in browser:
```
http://localhost:8000/index.html
```

### Option 2: Using Node.js

1. Install http-server globally:
```bash
npm install -g http-server
```

2. Navigate to website folder and run:
```bash
cd website
http-server -p 8000
```

3. Open in browser:
```
http://localhost:8000/index.html
```

## Pages Overview

### Home Page (index.html)
- Hero section with call-to-action
- Feature overview cards
- Statistics section
- Final CTA section

### Features Page (features.html)
- Detailed explanation of each feature:
  - Campaign Dashboard
  - Voter Management
  - Pledge Tracking
  - Event Management
  - Call Management
  - Agent Management
  - Zero Day Management (Ballot Boxes)
  - Real-time Messaging
- Each feature includes:
  - How it works
  - Benefits and efficiency gains
  - Visual mockups/examples

### Pricing Page (pricing.html)
- Three pricing tiers (Basic, Professional, Enterprise)
- Feature comparison table
- FAQ section

### About Page (about.html)
- Mission statement
- Why the system was built
- Key differentiators
- Company values

### Contact Page (contact.html)
- Contact form
- Contact information
- Process overview

## Design Features

- Uses the same color scheme as the main application (#6fc1da primary color)
- Responsive design for mobile, tablet, and desktop
- Smooth animations and transitions
- Professional, modern UI
- Consistent branding throughout

## Customization

### Update Contact Information
Edit the contact details in:
- `index.html` (footer)
- `contact.html` (contact info section)
- All other pages (footer sections)

### Update Pricing
Edit pricing in `pricing.html`:
- Pricing cards section
- Feature comparison table

### Add/Remove Features
Edit `features.html` to add or modify feature descriptions.

## Notes

- The contact form currently shows a success message but doesn't actually send emails. You'll need to integrate with a backend service or email API.
- All images and icons are using SVG or CSS-generated graphics. Replace with actual screenshots if desired.
- The website is fully static and can be hosted on any web server or CDN.

