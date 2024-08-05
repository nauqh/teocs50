from hikari import Embed


def noti_embed(title, description, url, author):
    return Embed(
        title=title,
        description=description,
        color="#118ab2",
        url=url
    ).set_footer(
        text=f"Posted by {author.global_name}",
        icon=author.avatar_url
    )
