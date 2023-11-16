# Photon Laser Tag System

The main project repository for CSCE 3513 - Software Engineering. This contains all the source code and (maybe) an executable for all distributions of the software. Right now, it is still being developed, but a road map of features will be included to show where we are at.

#### by LaserByte - Team 8
##### Last updated 11/16/2023

## How to use

Make sure Python 3.9+ is installed.
It is highly recommended to use a Python virtual environment. To create one, use:

`python -m venv /path/to/virtual/environment`

Then navigate to the environment's `/Scripts` folder and run `activate` (Mac/Linux) or `activate.bat` (Windows)

Here are the libraries used:
- `pip install kivy[full]`
- `pip install supabase`
- `pip install python-dotenv`

Then, download and put `.env` from the Slack into the root folder.

Finally, run the program using `python main.py`

### Testing

If you want to use our traffic generator, please use [this repo](https://github.com/UARK-LaserByte/udp-tests) as it allows for better testing (or you can use your own if you want because it just needs traffic on the UDP ports)

## Road Map

**Sprint #1**:
- Deciding on which language to use (Python)
- Creating all the communication channels
- Submitting the first draft of design document

**Sprint #2**:
- Setting up a SupaBase database to handle storage and software communications
- Creating the splash screen and player entry screen
- Setting up UDP sockets and testing a full game without UI
- Updating the design document to full define the expectations of the project

**Sprint #3**:
- Finishing the screen flow and fixing any bugs with player entry screen
- Creating the countdown screen and player action screen
- Finishing UDP interactions
- Finishing the design document
- Standardizing the UI for the entire application

**Sprint #4**:
- Finishing the project
- Adding UI tweaks
- Make the game loop
- Fix any bugs

## Design Document

[Design Document](https://uark-my.sharepoint.com/:w:/g/personal/alprosse_uark_edu/EUoDgCKoJAlBvLPaeWUmcOABm5QC2ipi3dcoMTviTl-DhA?e=DnYhJe)

This design document describes what the Photon Laser Tag system should do and how we would implement them

## Open Source Libraries

It currently uses:
- [Kivy](https://kivy.org/) for the cross-platform GUI rendering.
- [Supabase](https://supabase.com/) for database management.
- [dotenv](https://pypi.org/project/python-dotenv/) for reading environment variables.
