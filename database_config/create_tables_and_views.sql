USE [home]
GO
/****** Objeto: Table [dbo].[Temperature] Fecha de script: 27/10/2026 17:57:22 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Temperature](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[id_device] [varchar](255) NOT NULL,
	[temperature] [float] NOT NULL,
	[created_at] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Objeto: View [dbo].[vw_Temperature] Fecha de script: 27/10/2026 17:57:22 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

-- ==========================================
-- 2. CREACIÓN DE VISTAS
-- ==========================================

CREATE VIEW [dbo].[vw_Temperature] AS
SELECT 
    id,
    id_device,
    temperature,
    created_at
FROM Temperature;

GO
/****** Objeto: Table [dbo].[Humidity] Fecha de script: 27/10/2026 17:57:22 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Humidity](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[id_device] [varchar](255) NOT NULL,
	[humidity] [float] NOT NULL,
	[created_at] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Objeto: View [dbo].[vw_Humidity] Fecha de script: 27/10/2026 17:57:22 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[vw_Humidity] AS
SELECT 
    id,
    id_device,
    humidity,
    created_at
FROM Humidity;

GO
/****** Objeto: Table [dbo].[Luminosity] Fecha de script: 27/10/2026 17:57:22 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Luminosity](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[id_device] [varchar](255) NOT NULL,
	[luminosity] [float] NOT NULL,
	[created_at] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Objeto: View [dbo].[vw_Luminosity] Fecha de script: 27/10/2026 17:57:22 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[vw_Luminosity] AS
SELECT 
    id,
    id_device,
    luminosity,
    created_at
FROM Luminosity;

GO
/****** Objeto: Table [dbo].[LightStatus] Fecha de script: 27/10/2026 17:57:22 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LightStatus](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[room] [varchar](100) NOT NULL,
	[status] [varchar](50) NOT NULL,
	[created_at] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Objeto: View [dbo].[vw_LightStatus] Fecha de script: 27/10/2026 17:57:22 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[vw_LightStatus] AS
SELECT 
    id,
    room,
    status,
    created_at
FROM LightStatus;

GO
/****** Objeto: Table [dbo].[MusicPlayed] Fecha de script: 27/10/2026 17:57:22 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[MusicPlayed](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[song] [varchar](255) NOT NULL,
	[created_at] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Objeto: View [dbo].[vw_MusicPlayed] Fecha de script: 27/10/2026 17:57:22 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[vw_MusicPlayed] AS
SELECT 
    id,
    song,
    created_at
FROM MusicPlayed;

GO
/****** Objeto: Table [dbo].[PersonsRegistered] Fecha de script: 27/10/2026 17:57:22 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[PersonsRegistered](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[person_name] [varchar](255) NOT NULL,
	[created_at] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Objeto: View [dbo].[vw_PersonsRegistered] Fecha de script: 27/10/2026 17:57:22 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[vw_PersonsRegistered] AS
SELECT 
    id,
    person_name,
    created_at
FROM PersonsRegistered;

GO
/****** Objeto: Table [dbo].[HomeStatus] Fecha de script: 27/10/2026 17:57:22 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[HomeStatus](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[status] [varchar](100) NOT NULL,
	[created_at] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Objeto: View [dbo].[vw_HomeStatus] Fecha de script: 27/10/2026 17:57:22 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[vw_HomeStatus] AS
SELECT 
    id,
    status,
    created_at
FROM HomeStatus;

GO
/****** Objeto: Table [dbo].[LedStatus] Fecha de script: 27/10/2026 17:57:22 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LedStatus](
	[id_led_status] [int] IDENTITY(1,1) NOT NULL,
	[room] [varchar](100) NOT NULL,
	[status] [varchar](3) NOT NULL,
	[created_at] [datetime] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id_led_status] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Objeto: Table [dbo].[Memories] Fecha de script: 27/10/2026 17:57:22 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Memories](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[id_user] [varchar](255) NOT NULL,
	[role] [varchar](50) NOT NULL,
	[content] [nvarchar](max) NOT NULL,
	[reasoning_details] [nvarchar](max) NULL,
	[model] [varchar](100) NULL,
	[created_at] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
ALTER TABLE [dbo].[HomeStatus] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[Humidity] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[LedStatus] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[LightStatus] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[Luminosity] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[Memories] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[MusicPlayed] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[PersonsRegistered] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[Temperature] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[LedStatus]  WITH CHECK ADD CHECK  (([status]='OFF' OR [status]='ON'))
GO
