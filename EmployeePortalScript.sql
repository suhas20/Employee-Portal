USE [master]
GO

/****** Object:  Database [EmployeePortal]    Script Date: 08-06-2024 04:20:36 ******/
CREATE DATABASE [EmployeePortal]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'EmployeePortal', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.SQLEXPRESS01\MSSQL\DATA\EmployeePortal.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'EmployeePortal_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.SQLEXPRESS01\MSSQL\DATA\EmployeePortal_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO

IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [EmployeePortal].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO

ALTER DATABASE [EmployeePortal] SET ANSI_NULL_DEFAULT OFF 
GO

ALTER DATABASE [EmployeePortal] SET ANSI_NULLS OFF 
GO

ALTER DATABASE [EmployeePortal] SET ANSI_PADDING OFF 
GO

ALTER DATABASE [EmployeePortal] SET ANSI_WARNINGS OFF 
GO

ALTER DATABASE [EmployeePortal] SET ARITHABORT OFF 
GO

ALTER DATABASE [EmployeePortal] SET AUTO_CLOSE OFF 
GO

ALTER DATABASE [EmployeePortal] SET AUTO_SHRINK OFF 
GO

ALTER DATABASE [EmployeePortal] SET AUTO_UPDATE_STATISTICS ON 
GO

ALTER DATABASE [EmployeePortal] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO

ALTER DATABASE [EmployeePortal] SET CURSOR_DEFAULT  GLOBAL 
GO

ALTER DATABASE [EmployeePortal] SET CONCAT_NULL_YIELDS_NULL OFF 
GO

ALTER DATABASE [EmployeePortal] SET NUMERIC_ROUNDABORT OFF 
GO

ALTER DATABASE [EmployeePortal] SET QUOTED_IDENTIFIER OFF 
GO

ALTER DATABASE [EmployeePortal] SET RECURSIVE_TRIGGERS OFF 
GO

ALTER DATABASE [EmployeePortal] SET  DISABLE_BROKER 
GO

ALTER DATABASE [EmployeePortal] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO

ALTER DATABASE [EmployeePortal] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO

ALTER DATABASE [EmployeePortal] SET TRUSTWORTHY OFF 
GO

ALTER DATABASE [EmployeePortal] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO

ALTER DATABASE [EmployeePortal] SET PARAMETERIZATION SIMPLE 
GO

ALTER DATABASE [EmployeePortal] SET READ_COMMITTED_SNAPSHOT OFF 
GO

ALTER DATABASE [EmployeePortal] SET HONOR_BROKER_PRIORITY OFF 
GO

ALTER DATABASE [EmployeePortal] SET RECOVERY SIMPLE 
GO

ALTER DATABASE [EmployeePortal] SET  MULTI_USER 
GO

ALTER DATABASE [EmployeePortal] SET PAGE_VERIFY CHECKSUM  
GO

ALTER DATABASE [EmployeePortal] SET DB_CHAINING OFF 
GO

ALTER DATABASE [EmployeePortal] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO

ALTER DATABASE [EmployeePortal] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO

ALTER DATABASE [EmployeePortal] SET DELAYED_DURABILITY = DISABLED 
GO

ALTER DATABASE [EmployeePortal] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO

ALTER DATABASE [EmployeePortal] SET QUERY_STORE = OFF
GO

ALTER DATABASE [EmployeePortal] SET  READ_WRITE 
GO


USE [EmployeePortal]
GO

/****** Object:  Table [dbo].[EmpAccounts]    Script Date: 08-06-2024 04:20:59 ******/
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


USE [EmployeePortal]
GO

/****** Object:  Table [dbo].[Employees]    Script Date: 08-06-2024 04:21:05 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Employees](
	[EmpID] [varchar](50) NOT NULL,
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


USE [EmployeePortal]
GO

/****** Object:  Table [dbo].[Leaves]    Script Date: 08-06-2024 04:21:12 ******/
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

ALTER TABLE [dbo].[Leaves]  WITH CHECK ADD  CONSTRAINT [FK_Leaves_Employees] FOREIGN KEY([EmpID])
REFERENCES [dbo].[Employees] ([EmpID])
GO

ALTER TABLE [dbo].[Leaves] CHECK CONSTRAINT [FK_Leaves_Employees]
GO


USE [EmployeePortal]
GO

/****** Object:  Table [dbo].[Leaves]    Script Date: 08-06-2024 04:21:12 ******/
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

ALTER TABLE [dbo].[Leaves]  WITH CHECK ADD  CONSTRAINT [FK_Leaves_Employees] FOREIGN KEY([EmpID])
REFERENCES [dbo].[Employees] ([EmpID])
GO

ALTER TABLE [dbo].[Leaves] CHECK CONSTRAINT [FK_Leaves_Employees]
GO


USE [EmployeePortal]
GO

/****** Object:  Table [dbo].[ShiftRequest]    Script Date: 08-06-2024 04:21:19 ******/
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


USE [EmployeePortal]
GO

/****** Object:  Table [dbo].[Tasks]    Script Date: 08-06-2024 04:21:26 ******/
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

ALTER TABLE [dbo].[Tasks]  WITH CHECK ADD  CONSTRAINT [FK_Tasks_Employees] FOREIGN KEY([AssignedTo])
REFERENCES [dbo].[Employees] ([EmpID])
GO

ALTER TABLE [dbo].[Tasks] CHECK CONSTRAINT [FK_Tasks_Employees]
GO


USE [EmployeePortal]
GO

/****** Object:  Table [dbo].[Timesheet]    Script Date: 08-06-2024 04:21:33 ******/
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

ALTER TABLE [dbo].[Timesheet]  WITH CHECK ADD  CONSTRAINT [FK_Timesheet_Employees] FOREIGN KEY([EmpID])
REFERENCES [dbo].[Employees] ([EmpID])
GO

ALTER TABLE [dbo].[Timesheet] CHECK CONSTRAINT [FK_Timesheet_Employees]
GO


