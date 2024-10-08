USE [EmployeePortal]
GO
/****** Object:  Table [dbo].[assignee]    Script Date: 06-09-2024 17:34:11 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[assignee](
	[AssignID] [varchar](50) NOT NULL,
	[ClientID] [varchar](50) NULL,
	[TrainerID] [varchar](50) NULL,
 CONSTRAINT [PK_assignee] PRIMARY KEY CLUSTERED 
(
	[AssignID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[EmpAccounts]    Script Date: 06-09-2024 17:34:11 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[EmpAccounts](
	[EmpAccID] [varchar](50) NOT NULL,
	[EmpEmail] [varchar](50) NOT NULL,
	[EmpPassword] [varchar](50) NOT NULL,
	[EmpName] [varchar](50) NOT NULL,
	[EmpUsername] [varchar](50) NOT NULL,
	[IsAdmin] [int] NOT NULL,
 CONSTRAINT [PK_EmpAccounts] PRIMARY KEY CLUSTERED 
(
	[EmpAccID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Employees]    Script Date: 06-09-2024 17:34:11 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Employees](
	[EmpID] [varchar](50) NOT NULL,
	[EmpAccID] [varchar](50) NOT NULL,
	[EmpName] [varchar](50) NOT NULL,
	[EmpShift] [varchar](50) NULL,
	[EmpStartDate] [date] NOT NULL,
	[EmpToDate] [date] NOT NULL,
 CONSTRAINT [PK_Employees] PRIMARY KEY CLUSTERED 
(
	[EmpID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Feedback]    Script Date: 06-09-2024 17:34:11 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Feedback](
	[FeedbackID] [varchar](50) NOT NULL,
	[ClientName] [varchar](50) NOT NULL,
	[TrainerName] [varchar](50) NOT NULL,
	[Message] [varchar](max) NOT NULL,
	[Date] [date] NOT NULL,
 CONSTRAINT [PK_Feedback] PRIMARY KEY CLUSTERED 
(
	[FeedbackID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Leaves]    Script Date: 06-09-2024 17:34:11 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Leaves](
	[ID] [varchar](50) NOT NULL,
	[EmpID] [varchar](50) NOT NULL,
	[EmpName] [varchar](50) NOT NULL,
	[EmpEmail] [varchar](50) NOT NULL,
	[FromDate] [date] NOT NULL,
	[ToDate] [date] NOT NULL,
	[Status] [int] NOT NULL,
 CONSTRAINT [PK_Leaves] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Notifications]    Script Date: 06-09-2024 17:34:11 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Notifications](
	[NotificationID] [varchar](50) NOT NULL,
	[Message] [varchar](max) NOT NULL,
	[EmpID] [varchar](50) NOT NULL,
 CONSTRAINT [PK_Notifications] PRIMARY KEY CLUSTERED 
(
	[NotificationID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ShiftRequest]    Script Date: 06-09-2024 17:34:11 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ShiftRequest](
	[ShiftID] [varchar](50) NOT NULL,
	[EmpID] [varchar](50) NOT NULL,
	[EmpName] [varchar](50) NOT NULL,
	[EmpEmail] [varchar](50) NOT NULL,
	[Shift] [varchar](50) NOT NULL,
	[ForMonth] [varchar](50) NOT NULL,
	[Reason] [varchar](max) NULL,
	[Action] [int] NULL,
 CONSTRAINT [PK_ShiftRequest] PRIMARY KEY CLUSTERED 
(
	[ShiftID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Tasks]    Script Date: 06-09-2024 17:34:11 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Tasks](
	[TaskID] [varchar](50) NOT NULL,
	[AssignedTo] [varchar](50) NOT NULL,
	[CreatedOn] [date] NOT NULL,
	[ShortDescription] [varchar](50) NOT NULL,
	[WorkNotes] [varchar](max) NOT NULL,
 CONSTRAINT [PK_Tasks] PRIMARY KEY CLUSTERED 
(
	[TaskID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Timesheet]    Script Date: 06-09-2024 17:34:11 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Timesheet](
	[ID] [varchar](50) NOT NULL,
	[EmpID] [varchar](50) NOT NULL,
	[EmpName] [varchar](50) NOT NULL,
	[EmpEmail] [varchar](50) NULL,
	[FilledTimesheet] [varchar](50) NOT NULL,
	[Date] [date] NOT NULL,
	[Status] [int] NOT NULL,
 CONSTRAINT [PK_Timesheet] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[assignee]  WITH CHECK ADD  CONSTRAINT [FK_assignee_EmpAccounts] FOREIGN KEY([ClientID])
REFERENCES [dbo].[EmpAccounts] ([EmpAccID])
GO
ALTER TABLE [dbo].[assignee] CHECK CONSTRAINT [FK_assignee_EmpAccounts]
GO
ALTER TABLE [dbo].[assignee]  WITH CHECK ADD  CONSTRAINT [FK_assignee_Employees] FOREIGN KEY([TrainerID])
REFERENCES [dbo].[Employees] ([EmpID])
GO
ALTER TABLE [dbo].[assignee] CHECK CONSTRAINT [FK_assignee_Employees]
GO
ALTER TABLE [dbo].[Employees]  WITH CHECK ADD  CONSTRAINT [FK_Employees_EmpAccounts] FOREIGN KEY([EmpAccID])
REFERENCES [dbo].[EmpAccounts] ([EmpAccID])
GO
ALTER TABLE [dbo].[Employees] CHECK CONSTRAINT [FK_Employees_EmpAccounts]
GO
ALTER TABLE [dbo].[Leaves]  WITH CHECK ADD  CONSTRAINT [FK_Leaves_Employees] FOREIGN KEY([EmpID])
REFERENCES [dbo].[Employees] ([EmpID])
GO
ALTER TABLE [dbo].[Leaves] CHECK CONSTRAINT [FK_Leaves_Employees]
GO
ALTER TABLE [dbo].[Notifications]  WITH CHECK ADD  CONSTRAINT [FK_Notifications_Employees] FOREIGN KEY([EmpID])
REFERENCES [dbo].[Employees] ([EmpID])
GO
ALTER TABLE [dbo].[Notifications] CHECK CONSTRAINT [FK_Notifications_Employees]
GO
ALTER TABLE [dbo].[Tasks]  WITH CHECK ADD  CONSTRAINT [FK_Tasks_Employees] FOREIGN KEY([AssignedTo])
REFERENCES [dbo].[Employees] ([EmpID])
GO
ALTER TABLE [dbo].[Tasks] CHECK CONSTRAINT [FK_Tasks_Employees]
GO
ALTER TABLE [dbo].[Timesheet]  WITH CHECK ADD  CONSTRAINT [FK_Timesheet_Employees] FOREIGN KEY([EmpID])
REFERENCES [dbo].[Employees] ([EmpID])
GO
ALTER TABLE [dbo].[Timesheet] CHECK CONSTRAINT [FK_Timesheet_Employees]
GO
