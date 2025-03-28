def main():
    print("hello, I'm here!!!")


main()

# # Left: 📁 folder
# $env.PROMPT_COMMAND = {
#   let path = ($env.PWD | path basename)
#   $"📁 ($path) "
# }

# # Right: Display Git status
# $env.PROMPT_COMMAND_RIGHT = {
#     get_git_status
# }

# # Prompt symbol
# $env.PROMPT_INDICATOR = "➜ "


# 



#   let git_segment = (
#     if ($branch_name != "") {
#       [
#         (ansi { fg: $GIT_BG bg: $TERM_BG }) # color
#         (char -u e0b2) # 
#         (ansi { fg: $TERM_FG bg: $GIT_BG }) # color
#         (char space) # space
#         $repo_status # repo status
#         (ansi { fg: $TERM_FG bg: $GIT_BG }) # color
#         (char space)
#         (ansi { fg: "#4E9A06" bg: $GIT_BG }) # color
#         (char -u e0b2) # 
#         (ansi { fg: $TERM_BG bg: "#4E9A06" }) # color
#         (char space) # space
#         # (char -u f1d3)                       # 
#         # (char -u e0a0)                       # 
#         (char nf_git_branch) # 
#         (char space) # space
#         $branch_name # main
#         (char space) # space
#         ($R) # reset color
#       ] | str join
#     }
#   )