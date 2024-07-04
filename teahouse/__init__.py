import check50
import re


@check50.check()
def exists():
    """teahouse.R exists"""
    check50.exists("teahouse.R")


@check50.check(exists)
def readline():
    """teahouse.R uses readline"""
    with open("teahouse.R", "r") as f:
        contents = f.readlines()

    new_contents = replace_readline(contents)
    if new_contents == contents:
        raise check50.Failure(f"Could not find readline in teahouse.R")

    with open("teahouse.R", "w") as f:
        f.writelines(new_contents)


@check50.check(readline)
def green_tea():
    """teahouse.R correctly recommends green tea"""
    check_recommendation("Light", "Yes", "green tea")


@check50.check(green_tea)
def black_tea():
    """teahouse.R correctly recommends black tea"""
    check_recommendation("Bold", "Yes", "black tea")


@check50.check(black_tea)
def chamomile():
    """teahouse.R correctly recommends chamomile tea"""
    check_recommendation("Light", "No", "chamomile")


@check50.check(chamomile)
def rooibos():
    """teahouse.R correctly recommends rooibos tea"""
    check_recommendation("Bold", "No", "rooibos")


def check_recommendation(flavor: str, caffeine: str, tea: str) -> None:
    status = check50.run(f"Rscript teahouse.R {flavor} {caffeine}").exit()
    out = check50.run(f"Rscript teahouse.R {flavor} {caffeine}").stdout()

    if status != 0:
        raise check50.Failure(out)

    if tea.lower() not in out.lower():
        raise check50.Failure(
            f'Expected to find "{tea}" in output when entering "{flavor}" followed by "{caffeine}"'
        )


def replace_readline(contents: list[str]) -> list[str]:
    """Prepares an interactive R script to be run with command line arguments"""
    modified_contents = []
    readline_count = 0

    for line in contents:
        if match := re.search("readline", line):
            readline_count += 1

            start = match.start()
            open_paren = 0
            close_paren = 0
            for i in range(start, len(line)):
                if line[i] == "(":
                    open_paren += 1
                elif line[i] == ")":
                    close_paren += 1
                
                if open_paren > 0 and open_paren == close_paren:
                    end = i
                    break
            
            line = line[:start] + f"commandArgs(trailingOnly = TRUE)[{readline_count}]" + line[end + 1:]

        modified_contents.append(line)

    return modified_contents
