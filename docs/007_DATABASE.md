# LeadForgeAI — Database Architecture

Version: 1.0.0

Status: Draft

---

# Purpose

This document defines the complete database architecture of LeadForgeAI.

The database is the single source of truth.

Every module stores and retrieves data through the Backend API.

Direct database access from the frontend or workflow engine is strictly prohibited.

---

# Database Philosophy

The database should be:

Reliable

Normalized

Scalable

Easy to Maintain

Easy to Backup

Easy to Extend

Future SaaS Ready

---

# Database Engine

PostgreSQL

---

# Design Principles

Each table has one responsibility.

Avoid duplicated information.

Store relationships instead of repeating data.

Never store AI-generated information inside business tables.

Separate raw data from processed data.

---

# Primary Domains

LeadForgeAI is divided into independent domains.

Workspace

Business

People

Website

Contact

Campaign

Workflow

AI

System

Every future table belongs to one of these domains.

---

# Core Entities

Version 1 will begin with these core entities.

Workspace

Business

Person

Website

Email

Phone

Social Profile

Campaign

Workflow

AI Analysis

Settings

Activity Log

These entities form the foundation of the platform.

Future versions may introduce additional entities without breaking the architecture.

---

# Entity Relationships

Workspace

↓

Businesses

↓

People

↓

Websites

↓

Contacts

↓

AI Analysis

↓

Campaigns

↓

Activities

Every record belongs to exactly one Workspace.

No data should exist outside a Workspace.

---

# Workspace Isolation

Every workspace is completely isolated.

A workspace owns:

Businesses

People

Campaigns

Templates

Exports

History

Logs

AI Context

Settings

Deleting a workspace removes only that workspace's data.

Other workspaces remain unaffected.

---

# Data Lifecycle

Discovery

↓

Validation

↓

Storage

↓

Enrichment

↓

AI Analysis

↓

Campaign Usage

↓

Archive

↓

Deletion (optional)

The system should preserve historical information whenever practical.

---

# Soft Delete

LeadForgeAI should prefer soft deletion.

Deleted records are marked as deleted instead of immediately removed.

This protects users from accidental data loss.

Future versions may include automatic cleanup policies.

---

END OF PART 1

---

# Database Domains

LeadForgeAI organizes all data into independent domains.

Workspace Domain

Business Domain

People Domain

Website Domain

Contact Domain

AI Domain

Campaign Domain

Workflow Domain

System Domain

Each domain owns its own entities and responsibilities.

---

# Core Tables

The initial version of LeadForgeAI will contain the following primary tables.

## Workspace

Purpose

Represents a user workspace.

Stores:

Workspace Name

Description

Created Date

Status

Default Settings

---

## Business

Purpose

Represents a business or organization.

Stores:

Business Name

Category

Description

Google Rating

Review Count

Business Status

Created Source

Created Date

Updated Date

---

## Website

Purpose

Represents a website belonging to a business.

Relationship

One Business

↓

Many Websites

Stores:

Website URL

Domain

HTTPS Status

CMS (Future)

Technology Stack (Future)

Crawl Status

Last Crawled

---

## Email

Purpose

Stores every email discovered.

Relationship

One Website

↓

Many Emails

Stores:

Email Address

Email Type

Source

Confidence Score

Verification Status

Last Verified

---

## Phone

Purpose

Stores business phone numbers.

Relationship

Business

↓

Many Phone Numbers

Stores:

Phone Number

Country Code

Phone Type

Source

---

## Address

Purpose

Stores physical addresses.

Stores:

Country

State

City

Postal Code

Street

Latitude

Longitude

Google Maps URL

---

## Social Profile

Purpose

Stores social media profiles.

Stores:

Platform

URL

Username

Followers (Future)

Verified Status (Future)

---

## Person

Purpose

Stores publicly listed professionals.

Examples

Founder

CEO

Doctor

Lawyer

Principal

Director

Stores:

Full Name

Designation

Public Bio

Public Profile URL

---

## Campaign

Purpose

Represents outreach campaigns.

Stores:

Campaign Name

Campaign Type

Status

Start Date

End Date

Statistics

---

## Workflow

Purpose

Represents automation workflows.

Stores:

Workflow Name

Workflow Type

Current Status

Execution History

---

## AI Analysis

Purpose

Stores AI generated business intelligence.

Stores:

Business Summary

Pain Points

Lead Score

Recommended Services

Personalized Opening Line

Last Generated

---

## Activity Log

Purpose

Stores important application events.

Stores:

Timestamp

Event Type

Module

Description

Severity

---

# Relationship Overview

Workspace

↓

Business

↓

Website

↓

Email

↓

AI Analysis

Business

↓

Phone

Business

↓

Address

Business

↓

Social Profile

Business

↓

Person

Business

↓

Campaign

Campaign

↓

Workflow

---

# Relationship Rules

One Workspace

↓

Many Businesses

One Business

↓

Many Websites

One Business

↓

Many Emails

One Business

↓

Many Phones

One Business

↓

Many Social Profiles

One Business

↓

Many People

One Business

↓

Many AI Analyses

One Campaign

↓

Many Businesses

One Workflow

↓

Many Executions

---

# Database Rule

Every table must have:

Primary Key

Created At

Updated At

Workspace ID (where applicable)

Soft Delete Flag

Future migrations must preserve backward compatibility whenever possible.

---

END OF PART 2

---

# Database Standards

This section defines mandatory rules that every database table must follow.

These rules are permanent unless a future architecture version explicitly replaces them.

---

# Primary Keys

Every table must use UUID as the primary key.

Reason:

Global uniqueness

Easy synchronization

Future SaaS support

Future offline synchronization

No integer auto increment IDs.

---

# Foreign Keys

Every relationship must use foreign keys.

Example

Business

↓

Website

↓

Email

↓

AI Analysis

No table should reference another table using text fields.

---

# Audit Fields

Every table must contain the following fields.

id

created_at

updated_at

deleted_at

created_by (Future)

updated_by (Future)

workspace_id (where applicable)

---

# Timestamp Standard

All timestamps must be stored in UTC.

The frontend is responsible for converting timestamps into the user's local timezone.

---

# Naming Convention

Table Names

Singular

Examples

workspace

business

website

email

campaign

workflow

Column Names

snake_case

Examples

business_name

created_at

updated_at

review_count

Never use spaces.

Never use camelCase.

---

# Boolean Naming

Boolean columns must always begin with:

is_

has_

Examples

is_active

is_verified

has_website

has_email

---

# Enum Strategy

Avoid hardcoded strings.

Use enumerations whenever possible.

Examples

Campaign Status

draft

running

paused

completed

failed

Lead Status

new

enriched

qualified

archived

---

# Soft Delete

Records should not be permanently deleted.

Instead:

deleted_at

receives a timestamp.

Active records always have:

deleted_at = NULL

---

# Data Integrity

Never duplicate information.

One source.

One owner.

One truth.

Example

Website URL belongs to Website table.

It must never be stored again inside Business.

---

# Indexing Strategy

Indexes should exist for:

workspace_id

business_id

website_id

campaign_id

created_at

updated_at

Frequently searched fields

Indexes should only be added when they improve query performance.

Avoid unnecessary indexes.

---

# Unique Constraints

Examples

Workspace Name

Unique inside one user.

Website URL

Unique per workspace.

Email Address

Unique per website.

Duplicate data should be prevented whenever practical.

---

# AI Data

AI generated content should never overwrite original data.

Always store:

Raw Data

↓

AI Output

Separately.

This allows regeneration in the future.

---

# File Storage

Large files should never be stored inside PostgreSQL.

Only metadata should be stored.

Examples

Logo

Screenshot

Export

Document

Actual files belong in file storage.

---

# Backup Philosophy

The database must support:

Daily Backup

Manual Backup

Workspace Export

Workspace Import

Future Cloud Backup

---

# Migration Strategy

Every schema modification must be version controlled.

Database migrations should be reversible whenever practical.

No breaking migration should be released without documentation.

---

# Performance Philosophy

Optimize for readability first.

Optimize for maintainability second.

Optimize for speed only after measurement.

Never introduce complexity without measurable benefit.

---

END OF PART 3