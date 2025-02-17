# UI Design
This document outlines the goals for the UI/Frontend team to create the UI
workflow, graphics, screen designs, and later coding for the U3Core
application:

## Overview
This document provides the UI/Frontend team with structured inputs to create
the workflow, screen designs, and interface for U3Core, which allows users to
convert existing cameras into an anomaly detection system for oil leakage,
water leakage, fire, or smoke detection.

## User Roles and Permissions
1. Admin User:
   - Can sign up, verify email with OTP, and access all features.
   - Can invite other users with view-only permissions.
2. Viewer User:
   - Has limited access with view-only permissions for specific parts of
   the application.
## Main Sections and UI Components
1. User Authentication
   - Sign-Up Screen:
     - Input fields for email, password, and confirmation.
     - “Sign Up” button triggers OTP verification.
   - OTP Verification Screen:
     - Input field for OTP.
     - Button to resend OTP.
     - Success message on verification, leading to the Admin Dashboard.
2. Dashboard (Admin Landing Page)
   - Quick Overview:
     - Brief summary of user’s sites, cameras, and recent alerts.
   - Navigation Menu:
     - Left sidebar with main navigation (Configuration, Alerts Console,
     Action Settings).
     - Expandable tree structure for “Sites” and “Cameras” management.
3. Configuration Tab
   - Purpose: Allows the admin to set up and manage sites, cameras, and AI Edge
   Gateway.
   - Tree Structure for Site Management:
     - Left sidebar (menu bar) with expandable items:
       - Sites (Site 1, Site 2, ... Site n).
       - Each site shows GPS coordinates and list of cameras.
       - Cameras nested under each site (Cam1, Cam2, ... Camn).
     - Add Site Button to create new sites with location/GPS details.
     - Add Camera Button within each site.
   - Site Configuration Screen:
     - Fields for Site Name, GPS Coordinates, and Site Description.
     - Save and Cancel buttons.
   - Camera Configuration Screen:
     - Dropdown to assign Camera to Site.
     - Input fields for Camera ID, Model, and Location.
     - Dropdown to assign the camera to an AI Edge Gateway.
     - Save and Cancel buttons.
   - Gateway Mapping Screen:
     - Dropdown menu for selecting available AI Edge Gateways.
     - Mapping options to assign multiple cameras to a single gateway.
     - Summary view for current mappings (cameras to gateway).
4. Alerts Console Tab
    - Purpose: Provides a quick summary of all active alerts.
   - Alerts Summary Table:
     - Columns:
       - Site Name
       - Site Location
       - Camera ID
       - Reported Fault Type (e.g., Oil Leak, Water Leak, Fire,
       Smoke)
       - Timestamp of the alert
       - Link to video and a picture of the reported event
     - Filter and Search Options for easy sorting by site, fault type, or
     date.
     - Clickable rows to expand alert details in a new window or modal.
5. Action Settings Tab
   - Purpose: Enables configuring actions to be triggered when an alert is reported.
   - Action Configuration Screen:
     - Matrix for configuring alert response channels:
     - SMS, Email, WhatsApp, Twitter.
   - Option to set recipients for each alert type:
     - All Alerts – single group of recipients.
     - Custom Alerts – different recipients based on alert type.
   - Recipient Management:
     - Input fields for adding recipients' contact information.
     - Option to specify alert type per recipient (e.g., oil leaks to
     one group, fire alerts to another).
   - Save and Cancel buttons. 
## Suggested UI Workflows
1. User Onboarding (Sign-Up and OTP Verification):
   - Flow: User Sign-Up > OTP Verification > Redirect to Admin
   Dashboard.
2. Configuration Workflow:
   - Flow: Navigate to Configuration Tab > Add Site > Configure Site >
   Add Cameras > Assign Cameras to AI Edge Gateway.
3. Alert Management:
   - Flow: Navigate to Alerts Console > View Summary of Alerts >
   Filter/Search Alerts > Expand for Detailed Alert Information.
4. Action Configuration Workflow:
   - Flow: Navigate to Action Settings > Define Alert Channels >
   Add/Edit Recipients > Assign Alerts to Specific Recipients > Save. 
## Design Considerations
   - Color Coding for Alerts: Distinct colors for different alert types (e.g.,
   red for fire, blue for water leakage) to quickly identify issues.
   - Icons and Visuals:
     - Site and Camera icons in tree structure for easier identification.
     - Alert icons to signify fault types in the Alerts Console.
   - Responsive Design:
     - Ensure usability on both desktop and mobile devices, especially for
     viewing alerts and notifications.