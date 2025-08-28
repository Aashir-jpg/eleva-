# Eleva - Printing Shop Platform

## Project Overview
A full-stack web platform connecting printing shops with customers, built with React, Express, and PostgreSQL. The platform enables customers to find printing shops, place custom print orders with file uploads, and track order status.

## Architecture

### Frontend (React + Vite)
- **Framework**: React 18 with TypeScript
- **Routing**: Wouter for client-side routing
- **State Management**: TanStack Query for server state, React Context for auth
- **UI Components**: shadcn/ui with Tailwind CSS
- **Forms**: React Hook Form with Zod validation
- **File Handling**: Custom file upload component

### Backend (Express + Node.js)
- **Framework**: Express with TypeScript
- **Database**: PostgreSQL with Drizzle ORM
- **Authentication**: Passport.js with session-based auth
- **File Storage**: File uploads to local storage (ready for cloud integration)
- **Session Store**: PostgreSQL session store

### Database Schema
- **Users**: Handles both customers and shop owners (isShop flag)
- **Shops**: Extended shop information (description, services)
- **Orders**: Customer orders with file attachments, specifications, and status tracking

## Features Implemented

### Authentication
✓ User registration and login
✓ Session-based authentication with PostgreSQL store
✓ Protected routes
✓ Separate customer and shop account types

### Shop Management
✓ Shop listing with search/filtering
✓ Shop detail pages
✓ Shop profile information display

### Order System
✓ Order placement with file uploads
✓ Order specifications and quantity
✓ Order status tracking
✓ Order history for both customers and shops

### UI/UX
✓ Responsive design (mobile, tablet, desktop)
✓ Loading states and error handling
✓ Toast notifications
✓ Professional design with shadcn/ui components

## Current Database Status
- Using PostgreSQL with Drizzle ORM
- Database schema defined and migrations ready
- Session storage configured

## Recent Changes
- Database integration completed
- File upload functionality implemented
- Order placement system working
- Authentication system fully functional

## User Preferences
No specific preferences documented yet.

## Next Steps
- Payment integration (Stripe)
- Real-time order status updates
- File storage optimization
- Advanced shop filtering
- Review and rating system
