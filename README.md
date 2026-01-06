# HOS Compliance Toolkit: Interstate Truck Driver’s Guide

This repository provides a digital framework and compliance logic based on the **Hours of Service (HOS) regulations** found in part 395 of title 49 of the Code of Federal Regulations (CFR) [1]. These regulations are developed and enforced by the **Federal Motor Carrier Safety Administration (FMCSA)** [1].

## 1. Applicability and Scope
The logic in this toolkit applies to drivers of **property-carrying commercial motor vehicles (CMVs)** operating in interstate commerce [2, 3]. Compliance is mandatory if the vehicle weighs 10,001 pounds or more, or is transporting hazardous materials requiring placards [3]. Interstate commerce includes transportation between a place in a State and a place outside of such State, or between two places in a State through another State [4, 5].

## 2. Core Driving Limits
The system implements three primary maximum duty limits that must be followed at all times [6]:

*   **11-Hour Driving Limit:** Drivers are allowed to drive a maximum of 11 total hours after 10 consecutive hours off duty [7].
*   **14-Hour Driving Window:** This is a consecutive 14-hour period that begins when a driver starts any kind of work [6]. Driving is prohibited once this limit is reached until the driver has been off duty for 10 consecutive hours [6].
*   **30-Minute Rest Break:** A 30-minute consecutive break is required after 8 cumulative hours of driving [8]. This break can be taken as on-duty (not driving), off-duty, or in a sleeper berth [8].

## 3. Weekly Limits and Restarts
The toolkit tracks cumulative on-duty time over a rolling period [9]:
*   **60/70-Hour Limit:** Drivers may not drive after being on duty for 60 hours in 7 days (for companies not operating every day) or 70 hours in 8 days (for companies operating every day) [10, 11].
*   **34-Hour Restart:** Drivers can reset their cumulative weekly hours to zero by taking 34 or more consecutive hours off duty or in a sleeper berth [12].

## 4. Sleeper Berth Provisions
Drivers can obtain the required 10 hours of off-duty time using a sleeper berth [13, 14]. 
*   **Full Rest:** 10 consecutive hours in the sleeper berth completely restarts the 11 and 14-hour clocks [14].
*   **Split Option:** Drivers may pair a period of at least 7 consecutive hours in the sleeper berth with another period of at least 2 hours (off-duty or sleeper berth) to total 10 hours [15]. When paired, neither period counts against the 14-hour driving window [15].

## 5. Exceptions
The toolkit includes logic for specific regulatory exceptions:
*   **Adverse Driving Conditions:** Provides up to 2 additional hours of driving time and extends the 14-hour window by 2 hours for unforeseen conditions like fog or crashes [16, 17].
*   **150 Air-Mile Short-Haul:** Drivers operating within a 150 air-mile radius who return to their work location within 14 hours may be exempt from keeping standard logs and the 30-minute break [18-20].
*   **16-Hour Short-Haul:** Allows certain drivers to extend the 14-hour window to 16 hours once every 7 consecutive days if they return to their work reporting location [21].

## 6. Logging and Documentation
Most drivers must use an **Electronic Logging Device (ELD)** to maintain a **Record of Duty Status (RODS)** [22]. For manual logs, the documentation must include a 24-hour graph grid, total miles driven, vehicle numbers, and the carrier's name and office address [23-25]. Lines on the grid must clearly distinguish between Off-Duty, Sleeper Berth, Driving, and On-Duty (Not Driving) statuses [26].
