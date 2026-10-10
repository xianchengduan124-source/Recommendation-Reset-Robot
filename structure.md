# Project Overview

This project aims to build a robot/agent that helps users break free from recommendation algorithms. It does so by actively interfering with the user preference data that has been collected by these algorithms during previous usage.

---

## Desired Functions

### 1. Frontend (`./bilibili-frontend/`)

The frontend implements an automated script that allows the decision-maker to perform actions on the Bilibili website.

#### Required Features

- Automatic login
- Upvote, downvote, and favorite videos
- Collect user portrait and label information
- Watch or hover over a video for a specified duration
  - Watch videos in portrait or landscape mode
  - Hover over a video on the homepage (without entering the page)
  - Select videos from the recommendation list

#### Optional Features

- Upvote or downvote comments
- Stay on a page for a certain time (to simulate browsing/choosing behavior)
- Additional similar interactions

#### Data Extraction

The frontend must extract and translate all relevant data from the website into structured `#tags`, and, where possible, assign a `#weight` to each tag.

> Note: Support for other social media platforms may be added in the future.

---

### 2. Backend (`./decision-maker/`)

The backend implements a decision-making algorithm designed to counteract social media recommendation systems.

#### Core Objectives

- Increase the **variety and difference** between tags in the recommended content
- Reduce the **homogeneity** of recommendations
- Minimize total execution time by avoiding full video watches where possible

---

### 3. Data Exchange Between Frontend and Backend

#### Frontend → Backend

- `#tags` of videos, and their optional `#weight`
- Basic video metadata, including:
  - Video length
  - Whether the video is free to watch
  - Whether the creator is followed by the user
  - Whether and how many times the video has been watched by the user
- Global tag diversity during and after execution
- User reactions or replies to actions

#### Backend → Frontend

- Action instructions to be executed by the frontend
