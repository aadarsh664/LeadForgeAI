# LeadForgeAI

## AI Implementation Prompt

Read:

1. prompts/MASTER_IMPLEMENTATION_PROMPT.md

2. CONTEXT.md

3. tasks/TASK-009.md

Implement TASK-009 only.

---

Objective

Create the permanent Design System.

This Design System becomes the only source of UI components.

Future pages must never create duplicate UI.

---

Create

Design Tokens

Theme Provider

Typography System

Button Components

Input Components

Card Components

Feedback Components

Overlay Components

Utility Components

---

Rules

No Tailwind.

No Bootstrap.

No Material UI.

No Chakra UI.

No Ant Design.

Everything should be custom React components.

---

Icons

Lucide React only.

---

Typography

Primary

Inter

Fallback

Helvetica Neue

Helvetica

sans-serif

Never use Arial.

Developer Information

JetBrains Mono

---

Design Language

Apple Human Interface Guidelines

Linear

Raycast

Notion

Arc Browser

---

Colors

Neutral

Professional

Minimal

Accessible

No bright colors.

No gradients.

No glassmorphism.

---

Spacing

8px Grid.

---

Animations

150–250ms.

Smooth.

Professional.

---

Architecture

Every component reusable.

No duplicated CSS.

No inline styling unless necessary.

Prefer CSS Modules or organized global styling consistent with the project.

---

Output

Generate

TASK_COMPLETION_REPORT.md

GIT_DIFF_SUMMARY.md

Component Inventory

Created Files

Modified Files

Verification Steps

Wait for review.