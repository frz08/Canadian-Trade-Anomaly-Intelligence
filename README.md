# 🇨🇦 Canadian International Merchandise Trade Dashboard

An interactive business intelligence dashboard analyzing Canadian international merchandise trade data, built on Microsoft Fabric with Power BI. 

> 🚧 **Status: In Progress** — A working version is live. An expanded, more detailed version is actively being developed.

## 📌 Overview

This project delivers a fully interactive Power BI dashboard answering key business questions around Canada's import and export activity. Data is hosted in a Microsoft Fabric Lakehouse and flows through a modern data pipeline into a published Power BI report.

## 🏗️ Architecture

```
Statistics Canada Data
        ↓
Microsoft Fabric Lakehouse (OneLake)
        ↓
Dataflow Gen2 (Power Query Transformations)
        ↓
Semantic Model
        ↓
Power BI Report → Published to Fabric Workspace
```

## 🔍 What's Inside

- **Data Engineering** — Raw trade data ingested and stored in a Fabric Lakehouse
- **Transformations** — Data cleaned and shaped using Dataflow Gen2 with Power Query
- **Semantic Model** — Structured data model deployed for reporting
- **Dashboard** — Interactive Power BI report answering trade business questions

## 🛠️ Tools & Technologies

| Tool | Purpose |
|------|---------|
| Microsoft Fabric | Data platform and Lakehouse storage |
| Dataflow Gen2 | Data transformation with Power Query |
| Power BI | Dashboard and visualization |
| DAX | Measures and calculated columns |

## 📊 Business Questions Answered

- What are Canada's top export and import categories?
- Which trade partners dominate Canadian merchandise trade?
- How have trade volumes shifted over time?
- What seasonal patterns exist in Canadian trade activity?

## 🔗 Live Report

[View Dashboard](#) *https://app.powerbi.com/view?r=eyJrIjoiYzM1ZThiNDMtODgxMC00MjQ0LThlNzMtYjAyNjdlOWFmZGEyIiwidCI6ImY1MmYyMTgzLTlmNjctNGFkMi1iNjU2LTZmNzU0ZmUxOTZjYiIsImMiOjZ9*

---

*Developed by Farhaz Kolathoor*
