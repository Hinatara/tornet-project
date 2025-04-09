from .utils import GREEN, RED, WHITE, RESET, CYAN

def print_banner():
    banner = f"""
{WHITE} +-------------------------------------------------------+
{WHITE} |{GREEN} ████████╗ ██████╗ ██████╗ ███╗   ██╗███████╗████████╗{WHITE} |
{WHITE} |{GREEN} ╚══██╔══╝██╔═══██╗██╔══██╗████╗  ██║██╔════╝╚══██╔══╝{WHITE} |
{WHITE} |{GREEN}    ██║   ██║   ██║██████╔╝██╔██╗ ██║█████╗     ██║   {WHITE} |
{WHITE} |{GREEN}    ██║   ██║   ██║██╔══██╗██║╚██╗██║██╔══╝     ██║   {WHITE} |
{WHITE} |{GREEN}    ██║   ╚██████╔╝██║  ██║██║ ╚████║███████╗   ██║   {WHITE} |
{WHITE} |{GREEN}    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   {WHITE} |
{WHITE} +---------------------{CYAN}({RED}rewrite Hinatara{CYAN}){WHITE}----------------------+{RESET}
"""
    print(banner)