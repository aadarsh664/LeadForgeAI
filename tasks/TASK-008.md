# TASK-008

Title

Application Layout System

---

Status

Ready

---

Priority

Critical

---

Sprint

Sprint 2

---

Estimated Time

6-8 Hours

---

Objective

Build the permanent layout system of LeadForgeAI.

This layout becomes the foundation for every future screen.

After this task, every feature will plug into this layout.

---

Problem

Currently every screen replaces the entire application.

There is no reusable layout.

There is no navigation structure.

---

Goal

Create a reusable desktop layout.

Create Sidebar.

Create Top Bar.

Create Content Area.

Create Status Bar.

Create Layout Components.

---

Layout

+------------------------------------------------------------+

Top Bar

+------------+-----------------------------------------------+

Sidebar | Main Content

| |

| |

| |

+------------+-----------------------------------------------+

Status Bar

+------------------------------------------------------------+

---

Sidebar

Initially include

Dashboard

Workspace

Businesses

People

Campaigns

Automation

AI

Exports

Settings

Developer (Visible only in Developer Mode)

Icons only.

Labels below icons.

Future modules can be added easily.

---

Top Bar

Application Logo

Application Name

Current Workspace

Search Placeholder

Profile Placeholder

Developer Badge (Developer Mode Only)

---

Content Area

Displays selected page.

Initially use placeholder pages.

Example

Dashboard

Workspace

Businesses

Settings

Developer

Each page should have:

Title

Subtitle

Content Container

---

Status Bar

Display

Version

Current Mode

Connection Status

Current Time

Future Notifications Placeholder

---

Navigation

Sidebar navigation.

No routing library.

Internal state navigation only.

Future routing will be added later.

---

Backend

No backend changes required.

Use existing APIs.

---

Frontend

Create

Layout Component

Sidebar Component

Top Bar Component

Status Bar Component

Navigation Store

Page Components

---

Persistence

Remember last selected page.

Restore page after restart.

---

Animation

Sidebar hover

Page transition

Button hover

Selection indicator

Smooth animations

150–250 ms

---

Acceptance Criteria

Reusable Layout

Sidebar Navigation

Top Bar

Status Bar

Page Switching

Developer Mode Compatible

User Mode Compatible

---

Definition of Done

Layout Complete.

Navigation Working.

Persistence Working.

Desktop Integrated.

Committed.

---

Next Task

TASK-009

Design System Foundation

---

End of Task