import argparse
import tomllib

from time import timezone

def int_or_str(data):
    try:
        return int(data)
    except ValueError:
        return str(data)

def add_argument(argument, parser, ARGS):
    match argument:
        case "help":
            parser.add_argument(
            "--help",
            action="help",
            default=argparse.SUPPRESS,
            help="Show all script startup parameters and exit"
        )
            
        case "SILENT":
            parser.add_argument(
                "-s", "--silent",
                help="Do not open the created image or plot",
                action="store_const",
                const=not ARGS["SILENT"],
                default=ARGS["SILENT"],
                dest="SILENT"
            )

        case "IMAGE":
            parser.add_argument(
                "-i", "--image",
                help="Do not save plot image",
                action="store_const",
                const=not ARGS["IMAGE"],
                default=ARGS["IMAGE"],
                dest="IMAGE"
            )
            
        case "CUMULATIVE":
            parser.add_argument(
                "-c",
                help="Display staticics for all time or by week",
                action="store_const",
                const=not ARGS["CUMULATIVE"],
                default=ARGS["CUMULATIVE"],
                dest="CUMULATIVE",
            )
            
        case "HIDE_VOID":
            parser.add_argument(
                "-v",
                help="Hide void on the density or average plot",
                action="store_const",
                const=not ARGS["HIDE_VOID"],
                default=ARGS["HIDE_VOID"],
                dest="HIDE_VOID"
            )
            
        case "LABEL_TRESHOLD":
            parser.add_argument(
                "-t",
                help="Threshold for displaying the stage time on the main plot",
                default=ARGS["LABEL_TRESHOLD"],
                type=float,
                dest="LABEL_TRESHOLD"
            )
            
        case "AV_LABEL_TRESHOLD":
            parser.add_argument(
                "-avt",
                help="Threshold for displaying the stage time on the average plot",
                default=ARGS["AV_LABEL_TRESHOLD"],
                type=float,
                dest="AV_LABEL_TRESHOLD"
            )
            
        case "SHOW_LEGEND":
            parser.add_argument(
                "-l",
                help="Displaying the plot legend",
                action="store_const",
                const=not ARGS["SHOW_LEGEND"],
                default=ARGS["SHOW_LEGEND"],
                dest="SHOW_LEGEND"
            )
            
        case "LEGEND_COLUMNS":
            parser.add_argument(
                "-lc",
                help="Number of legend columns",
                dest="LEGEND_COLUMNS",
                type=int,
                default=ARGS["LEGEND_COLUMNS"],
            )
            
        case "START_RADIUS":
            parser.add_argument(
                "-r",
                help="Initial radius of the circle",
                dest="START_RADIUS",
                type=float,
                default=ARGS["START_RADIUS"],
            )
            
        case "IMAGE_SIDE":
            parser.add_argument(
                "-h",
                help="Image side size (width and height)",
                dest="IMAGE_SIDE",
                type=int_or_str,
                default=ARGS["IMAGE_SIDE"],
            )
            
        case "IMAGE_SCALE":
            parser.add_argument(
                "-x",
                help="Image size multiplier",
                dest="IMAGE_SCALE",
                type=int,
                default=ARGS["IMAGE_SCALE"],
            )
            
        case "PLOT_WIDTH":
            parser.add_argument(
                "-w",
                help="Plot width",
                dest="PLOT_WIDTH",
                type=float,
                default=ARGS["PLOT_WIDTH"],
            )
            
        case "PLOT_HEIGHT":
            parser.add_argument(
                "-h",
                help="Plot height",
                dest="PLOT_HEIGHT",
                type=float,
                default=ARGS["PLOT_HEIGHT"],
            )

def setup(script_name):
    settings = tomllib.load(open("settings.toml", "rb"))
    
    # Get settings
    ACTIVITIES = settings["activities"]
    ARGS = settings["global"] | settings[script_name]
    
    # Parse arguments
    parser = argparse.ArgumentParser(add_help=False)
    add_argument("help", parser, ARGS)
    
    for argument in ARGS:
        add_argument(argument, parser, ARGS)
    
    parsed_args = dict(parser.parse_args()._get_kwargs())
    for arg in parsed_args:
        ARGS[arg] = parsed_args[arg]
    
    # Setup auto settings    
    if "UTC_OFFSET" in ARGS and ARGS["UTC_OFFSET"] == "auto":
        ARGS["UTC_OFFSET"] = -timezone
        
    return ARGS, ACTIVITIES
