try:
    import os, requests, json, discord, time, random, string
    import forex_python.converter
    from Commands import *
    from bs4 import BeautifulSoup as bs
    from forex_python.converter import CurrencyRates

except:
    print("Error with modules.")
    raise


client = discord.Client()

with open("config.json") as file:
    config = json.load(file)
    file.close()

version = config["version"]

fpsite = ""

globalHeaders = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
}

token = config["token"]
prefix = config["prefix"]
discordinv = config["discordinv"]
client_id = config["client_id"]
stockxemail = config["stockxemail"]
stockxpass = config["stockxpass"]
stockx_api_url = config["stockx_api_url"]
stockx_base_url = config["stockx_base_url"]
goat_api_url = config["goat_api_url"]
goat_base_url = config["goat_base_url"]

currency_rates = CurrencyRates()


def error_embed(client, message, error):
    pass


def round_price(num):
    return round(num, 2)


def generate_address(base):
    uppercase_alphabet = string.ascii_uppercase
    addresses = []
    result = ""
    unit_names = ["Condo", "Unit", "Flr", "Apartment", "Apt", "Floor", "Suite"]
    for _ in range(20):
        prefix = (
            random.choice(uppercase_alphabet)
            + random.choice(uppercase_alphabet)
            + random.choice(uppercase_alphabet)
            + random.choice(uppercase_alphabet)
        )
        suffix = random.choice(unit_names) + " " + str(random.randint(1, 20))
        addresses.append(prefix + " " + base + " " + suffix + "\n")
    for address in addresses:
        result += address
    return result


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if not message.content:
        return

    if message.content.split()[0] == prefix + "ping":
        if len(message.content.split(" ")) != 1:
            embed = discord.Embed(title="FP Sneakers Bot")
            embed.add_field(
                name="Error", value="Invalid number of arguments.", inline=False
            )
            embed.set_footer(text="FP Sneakers | " + version)

            await message.channel.send(embed=embed)

        else:
            embed = discord.Embed(title="FP Sneakers Bot", color=0xA5F2F3)
            embed.set_thumbnail(url="https://i.imgur.com/O5HEApC.png")
            embed.add_field(
                name="Pong!", value="Bot is currently online.", inline=False
            )
            embed.set_footer(text="FP Sneakers | " + version)

            await message.channel.send(embed=embed)

    if message.content.split()[0] == prefix + "atc":
        try:
            if len(message.content.split(" ")) != 2:

                embed = discord.Embed(title="ATC Link Generator")
                embed.add_field(
                    name="Error", value="Invalid number of arguments.", inline=False
                )
                embed.set_footer(text="FP Sneakers | " + version)

                await message.channel.send(embed=embed)

            else:
                produrl = message.content.split(" ")[1]
                s = requests.session()
                prodobjr = s.get(produrl)
                srccode = prodobjr.text.split("var meta = ")[0]
                ogurl = srccode.split('<meta property="og:url" content="')[1]
                ogurl = ogurl.split('"')[0]
                prodtitle = srccode.split('<meta property="og:title" content="')[1]
                prodtitle = prodtitle.split('"')[0]
                thumbnail = srccode.split('<meta property="og:image" content="')[1]
                thumbnail = thumbnail.split('"')[0]
                ogprice = srccode.split('<meta property="og:price:amount" content="')[1]
                ogprice = ogprice.split('">')[0]
                ogcurrency = srccode.split(
                    '<meta property="og:price:currency" content="'
                )[1]
                ogcurrency = ogcurrency.split('"')[0]
                price = ogprice + " " + ogcurrency
                prodobj = prodobjr.text.split("var meta = ")[1]
                prodobj = prodobj.split(";")[0]
                prodobj = json.loads(prodobj)
                soup = bs(prodobjr.text, "html.parser")
                prodsiteLink = produrl.split("/")[2]
                prodsiteLink = "https://{}".format(prodsiteLink)

                embed = discord.Embed(title=prodtitle, url=ogurl, color=0x97C04A)
                embed.set_author(name="ATC Link Generator")
                embed.set_thumbnail(url="{}".format(thumbnail))
                embed.add_field(
                    name="Product ID", value="{}".format(prodobj["product"]["id"])
                )
                embed.add_field(name="Product Price", value=price, inline=True)
                for pid in prodobj["product"]["variants"]:
                    embed.add_field(
                        name="Size: " + str(pid["public_title"]),
                        value="**Link:** {}/cart/{}:1 \n**Variant: ** {}".format(
                            prodsiteLink, pid["id"], pid["id"]
                        ),
                    )
                embed.set_footer(text="FP Sneakers | " + version)

                await message.channel.send(embed=embed)
        except:
            embed = discord.Embed(title="ATC Link Generator")
            embed.add_field(
                name="Error", value="Could not execute scraper.", inline=False
            )
            embed.set_footer(text="FP Sneakers | " + version)

            await message.channel.send(embed=embed)

    if message.content.split()[0] == prefix + "stockx":
        if len(message.content.split(" ")) == 1:
            embed = discord.Embed(title="StockX Product Checker")
            embed.add_field(
                name="Error", value="Invalid number of arguments.", inline=False
            )
            embed.set_footer(text="FP Sneakers | " + version)

            await message.channel.send(embed=embed)
        else:
            product_name = message.content.split(prefix + "stockx ")[1]

            payload = {
                "x-algolia-agent": "Algolia for vanilla JavaScript 3.27.1",
                "x-algolia-api-key": "6bfb5abee4dcd8cea8f0ca1ca085c2b3",
                "x-algolia-application-id": "XW7SBCT9V6",
            }

            json_payload = {"params": "query={}&hitsPerPage=1".format(product_name)}

            r = requests.post(url=stockx_api_url, params=payload, json=json_payload)
            output = json.loads(r.text)

            product_name = ""
            thumbnail_url = ""
            product_url = ""
            release_date = ""
            style_id = ""
            highest_bid = ""
            lowest_ask = ""
            last_sale = ""
            # sales_last_72 = ''
            # deadstock_sold = ''
            retail_price = ""

            try:
                product_name = output["hits"][0]["name"]
                thumbnail_url = output["hits"][0]["thumbnail_url"]
                product_url = stockx_base_url + output["hits"][0]["url"]
                release_date = output["hits"][0]["release_date"]
                style_id = output["hits"][0]["style_id"]
                highest_bid = output["hits"][0]["highest_bid"]
                lowest_ask = output["hits"][0]["lowest_ask"]
                last_sale = output["hits"][0]["last_sale"]
                # sales_last_72 = output['hits'][0]['sales_last_72']
                # deadstock_sold = output['hits'][0]['deadstock_sold']
                retail_price = output["hits"][0]["searchable_traits"]["Retail Price"]
            except KeyError:
                pass
            except IndexError:
                embed = discord.Embed(title="StockX Product Checker")
                embed.add_field(
                    name="Error",
                    value="Could not fetch data from the API. Please try another product.",
                    inline=False,
                )
                embed.set_footer(text="FP Sneakers | " + version)

                await message.channel.send(embed=embed)
                raise

            r = requests.get(url=product_url)
            soup = bs(r.text, "html.parser")

            last_sale_size = ""
            lowest_ask_size = ""
            highest_bid_size = ""
            try:
                last_sale_size = (
                    soup.find("div", {"class": "last-sale-block"})
                    .find("span", {"class": "bid-ask-sizes"})
                    .text
                )
                lowest_ask_size = (
                    soup.find("div", {"class": "bid bid-button-b"})
                    .find("span", {"class": "bid-ask-sizes"})
                    .text
                )
                highest_bid_size = (
                    soup.find("div", {"class": "ask ask-button-b"})
                    .find("span", {"class": "bid-ask-sizes"})
                    .text
                )
            except AttributeError:
                pass

            try:
                usdprofit = last_sale - retail_price
                # usdprofitfee=usdprofit * .85-20
                usdprofit = round_price(usdprofit)
                cadprofit = currency_rates.convert("USD", "CAD", usdprofit)
                cadprofit = round_price(cadprofit)
            except TypeError:
                pass

            embed = discord.Embed(title="", url=product_url, color=4500277)
            embed.set_author(name="StockX Product Checker")
            embed.set_thumbnail(url=thumbnail_url)
            embed.add_field(
                name="Product Name",
                value="[{}]({})".format(product_name, product_url),
                inline=False,
            )
            embed.add_field(
                name="Retail Price", value="{} USD".format(retail_price), inline=True
            )
            embed.add_field(
                name="Release Date", value="{}".format(release_date), inline=True
            )
            embed.add_field(name="Style ID", value="{}".format(style_id), inline=True)
            embed.add_field(
                name="Last Sale",
                value="{} USD | {}".format(last_sale, last_sale_size),
                inline=True,
            )
            embed.add_field(
                name="Lowest Ask",
                value="{} USD | {}".format(lowest_ask, lowest_ask_size),
                inline=True,
            )
            embed.add_field(
                name="Highest Bid",
                value="{} USD | {}".format(highest_bid, highest_bid_size),
                inline=True,
            )
            try:
                embed.add_field(
                    name="USD Profit",
                    value="{} USD (fees not included)".format(usdprofit),
                    inline=True,
                )
                embed.add_field(
                    name="CAD Profit",
                    value="{} CAD (fees not included)".format(cadprofit),
                    inline=True,
                )
            except UnboundLocalError:
                embed.add_field(
                    name="USD Profit",
                    value="Error, not enough information",
                    inline=True,
                )
                embed.add_field(
                    name="CAD Profit",
                    value="Error, not enough information",
                    inline=True,
                )
            embed.set_footer(text="FP Sneakers | " + version)

            await message.channel.send(embed=embed)

    if message.content.split()[0] == prefix + "stockxfees":
        if len(message.content.split(" ")) != 4:
            embed = discord.Embed(title="StockX Fees Calculator")
            embed.add_field(
                name="Error", value="Invalid number of arguments.", inline=False
            )
            embed.set_footer(text="FP Sneakers | " + version)

            await message.channel.send(embed=embed)
        else:
            if message.content.split(" ")[1] not in ("us", "ca", "in"):
                embed = discord.Embed(title="StockX Fees Calculator")
                embed.add_field(
                    name="Error", value="Shipping region not recognized.", inline=False
                )
                embed.set_footer(text="FP Sneakers | " + version)

                await message.channel.send(embed=embed)
            else:
                shipping = 0.00
                if message.content.split(" ")[1] == "us":
                    shipping = 10.00  # $USD
                elif message.content.split(" ")[1] == "ca":
                    shipping = 20.00  # $USD
                elif message.content.split(" ")[1] == "in":
                    shipping = 30.00  # $USD

                percent_fees = (
                    float(message.content.split(" ")[2]) + 3.0
                )  # Transaction fee + 3% payment processing fee
                list_price = float(message.content.split(" ")[3])
                decimal_fees = percent_fees * 0.01
                fees_usd = list_price * decimal_fees
                raw_usd = list_price - fees_usd - shipping
                finalcad = round_price(currency_rates.convert("USD", "CAD", raw_usd))
                finalusd = round_price(raw_usd)

                embed = discord.Embed(title="StockX Fees Calculator", color=4500277)
                embed.set_thumbnail(url="https://i.imgur.com/bXlFT6c.jpg")
                embed.add_field(
                    name="Product List Price in USD",
                    value="${}".format(list_price),
                    inline=True,
                )
                embed.add_field(
                    name="Fees Percentage",
                    value="{}%".format(percent_fees),
                    inline=True,
                )
                embed.add_field(
                    name="Shipping Cost", value="${} USD".format(shipping), inline=True
                )
                embed.add_field(
                    name="Total Fees", value="${} USD".format(fees_usd), inline=True
                )
                embed.add_field(
                    name="Payout in USD", value="${} USD".format(finalusd), inline=True
                )
                embed.add_field(
                    name="Payout in CAD", value="${} CAD".format(finalcad), inline=True
                )
                embed.set_footer(text="FP Sneakers | " + version)

                await message.channel.send(embed=embed)

    if message.content.split()[0] == prefix + "goat":
        if len(message.content.split(" ")) == 1:
            embed = discord.Embed(title="Goat Product Checker")
            embed.add_field(
                name="Error", value="Invalid number of arguments.", inline=False
            )
            embed.set_footer(text="FP Sneakers | " + version)

            await message.channel.send(embed=embed)
        else:
            product_name = message.content.split(prefix + "goat ")[1]

            payload = {
                "x-algolia-agent": "Algolia for vanilla JavaScript 3.27.1",
                "x-algolia-api-key": "6bfb5abee4dcd8cea8f0ca1ca085c2b3",
                "x-algolia-application-id": "XW7SBCT9V6",
            }

            json_payload = {"params": "query={}&hitsPerPage=1".format(product_name)}

            r = requests.post(url=stockx_api_url, params=payload, json=json_payload)
            output = json.loads(r.text)

            retail_price = ""

            try:
                retail_price = output["hits"][0]["searchable_traits"]["Retail Price"]
            except:
                pass

            payload = {
                "x-algolia-agent": "Algolia for vanilla JavaScript 3.25.1",
                "x-algolia-api-key": "ac96de6fef0e02bb95d433d8d5c7038a",
                "x-algolia-application-id": "2FWOTDVM2O",
            }

            json_payload = {
                "params": "query=${}&hitsPerPage=1&facets=*".format(product_name)
            }

            r = requests.post(url=goat_api_url, params=payload, json=json_payload)

            data = json.loads(r.text)
            try:
                data = data["hits"][0]
            except:
                pass

            product_name = ""
            style_id = ""
            brand = ""
            release_date = ""
            product_url = ""
            original_picture_url = ""
            lowest_new_ask = ""
            lowest_used_ask = ""

            try:
                product_name = data["name"]
                style_id = data["sku"]
                brand = data["brand_name"]
                release_date = data["release_date"].split("T")[0]
                product_url = goat_base_url + data["slug"]
                original_picture_url = data["original_picture_url"]
                lowest_new_ask = data["new_lowest_price_cents"] / 100
                lowest_used_ask = data["used_lowest_price_cents"] / 100

            except KeyError:
                embed = discord.Embed(title="Goat Product Checker")
                embed.add_field(
                    name="Error",
                    value="Could not fetch data from the API. Please try another product.",
                    inline=False,
                )
                embed.set_footer(text="FP Sneakers | " + version)

                await message.channel.send(embed=embed)

            except IndexError:
                embed = discord.Embed(title="Goat Product Checker")
                embed.add_field(
                    name="Error",
                    value="Could not fetch data from the API. Please try another product.",
                    inline=False,
                )
                embed.set_footer(text="FP Sneakers | " + version)

                await message.channel.send(embed=embed)

            embed = discord.Embed(title="", url=product_url, color=0xFFFFFF)
            embed.set_author(name="Goat Product Checker")
            embed.set_thumbnail(url=original_picture_url)
            embed.add_field(
                name="Product Name",
                value="[{}]({})".format(product_name, product_url),
                inline=False,
            )
            try:
                embed.add_field(
                    name="Retail Price",
                    value="{} USD".format(retail_price),
                    inline=True,
                )
            except:
                embed.add_field(
                    name="Retail Price", value="{}".format("Unavailable"), inline=True
                )
            embed.add_field(
                name="Release Date", value="{}".format(release_date), inline=True
            )
            embed.add_field(name="Style ID", value="{}".format(style_id), inline=True)
            embed.add_field(name="Brand", value="{}".format(brand), inline=True)
            embed.add_field(
                name="Deadstock Lowest Ask",
                value="{} USD".format(lowest_new_ask),
                inline=True,
            )
            embed.add_field(
                name="Used Lowest Ask",
                value="{} USD".format(lowest_used_ask),
                inline=True,
            )
            embed.set_footer(text="FP Sneakers | " + version)

            await message.channel.send(embed=embed)

    if message.content.split()[0] == prefix + "supnycost":
        try:
            if len(message.content.split(" ")) != 2:
                embed = discord.Embed(title="Supreme Order Breakdown")
                embed.add_field(
                    name="Error", value="Invalid number of arguments.", inline=False
                )
                embed.set_footer(text="FP Sneakers | " + version)

                await message.channel.send(embed=embed)
            else:
                priceusd = float(message.content.split(" ")[1])
                taxrate = 0.3
                ship = 20.00
                taxes = taxrate * priceusd
                total = priceusd + ship + taxes
                totalcad = currency_rates.convert("USD", "CAD", total)
                embed = discord.Embed(
                    title="Supreme Order Breakdown",
                    url="http://www.supremenewyork.com/",
                    color=0xDA291C,
                )
                embed.set_thumbnail(url="https://i.imgur.com/NQmkI9O.png")
                embed.add_field(
                    name="Initial Price",
                    value="$" + str(round_price(priceusd)) + " USD",
                    inline=False,
                )
                embed.add_field(
                    name="Shipping & Handling",
                    value="$" + str(round_price(ship)) + " USD",
                    inline=False,
                )
                embed.add_field(
                    name="Taxes & Duties",
                    value="$" + str(round_price(taxes)) + " USD",
                    inline=False,
                )
                embed.add_field(
                    name="Order total in USD",
                    value="$" + str(round_price(total)),
                    inline=True,
                )
                embed.add_field(
                    name="Order total in CAD",
                    value="$" + str(round_price(totalcad)),
                    inline=True,
                )
                embed.set_footer(text="FP Sneakers | " + version)

                await message.channel.send(embed=embed)
        except:
            embed = discord.Embed(title="Supreme Order Breakdown")
            embed.add_field(
                name="Error", value="Price could not be calculated.", inline=False
            )
            embed.set_footer(text="FP Sneakers | " + version)

            await message.channel.send(embed=embed)

    if message.content.split()[0] == prefix + "shopifycheck":
        if len(message.content.split(" ")) != 2:
            embed = discord.Embed(title="Shopify Checker")
            embed.add_field(
                name="Error", value="Invalid number of arguments.", inline=False
            )
            embed.set_footer(text="FP Sneakers | " + version)

            await message.channel.send(embed=embed)
        elif "http" not in message.content.split(" ")[1]:
            embed = discord.Embed(title="Shopify Checker")
            embed.add_field(
                name="Error",
                value="Invalid URL (http must be included in the URL).",
                inline=False,
            )
            embed.set_footer(text="FP Sneakers | " + version)

            await message.channel.send(embed=embed)
        else:
            siteurl = message.content.split(" ")[1]
            try:

                s = requests.session()
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
                }
                sitesource = s.get(
                    message.content.split(" ")[1], headers=headers, timeout=15
                )
                if "Shopify" not in sitesource.text:
                    embed = discord.Embed(
                        title="FP Sneakers Shopify Checker", color=0x97C04A
                    )
                    embed.add_field(
                        name="{}".format(siteurl), value="Is probably not Shopify."
                    )
                    embed.set_footer(text="FP Sneakers | " + version)

                    await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="FP Sneakers Shopify Checker", color=0x97C04A
                    )
                    embed.set_thumbnail(url="https://i.imgur.com/s2stM43.png")
                    embed.add_field(
                        name="{}".format(siteurl), value="Is likely Shopify."
                    )
                    embed.set_footer(text="FP Sneakers | " + version)

                    await message.channel.send(embed=embed)
            except:
                embed = discord.Embed(title="Shopify Checker")
                embed.add_field(
                    name="Error", value="Failed to check site.", inline=False
                )
                embed.set_footer(text="FP Sneakers | " + version)

                await message.channel.send(embed=embed)

    if message.content.split()[0] == prefix + "supweek":
        if len(message.content.split(" ")) != 1:
            embed = discord.Embed(title="Supreme Week")
            embed.add_field(
                name="Error", value="Invalid number of arguments.", inline=False
            )
            embed.set_footer(text="FP Sneakers | " + version)

            await message.channel.send(embed=embed)
        else:
            pageSource = requests.get(
                "https://www.supremecommunity.com/season/spring-summer2018/droplists/"
            )
            pageSource = pageSource.content
            soup = bs(pageSource, "html.parser")
            links = soup.find_all("a", {"class": "block"})[0]
            link = (
                "https://www.supremecommunity.com"
                + str(links).split('href="')[1].split('">')[0]
            )
            embed = discord.Embed(
                title="Click here to see the items for the current Supreme week",
                url=link,
                color=0xDA291C,
            )
            embed.set_author(name="Supreme Week")
            embed.set_thumbnail(
                url="https://upload.wikimedia.org/wikipedia/commons/2/23/Supreme-logo-newyork.png"
            )
            embed.set_footer(text="FP Sneakers | " + version)

            await message.channel.send(embed=embed)

    if message.content.split()[0] == prefix + "addy":
        if len(message.content.split(" ")) == 1:
            embed = discord.Embed(title="Jigged Address Generator")
            embed.add_field(
                name="Error", value="Invalid number of arguments.", inline=False
            )
            embed.set_footer(text="FP Sneakers | " + version)

            await message.channel.send(embed=embed)
        else:
            try:
                base_address = message.content.split(prefix + "addy ")[1]
                generated_addresses = generate_address(base_address)
                embed = discord.Embed(title="Jigged Address Generator", color=0xDEB887)
                embed.add_field(
                    name="Addresses", value=generated_addresses, inline=False
                )
                embed.set_footer(text="FP Sneakers | " + version)

                await message.channel.send(embed=embed)
            except:
                embed = discord.Embed(title="Jigged Address Generator")
                embed.add_field(
                    name="Error",
                    value="Invalid address or too many values.",
                    inline=False,
                )
                embed.set_footer(text="FP Sneakers | " + version)

                await message.channel.send(embed=embed)

    if message.content.split()[0] == prefix + "inv":
        if len(message.content.split(" ")) != 1:
            embed = discord.Embed(title="FP Sneakers Discord Invite")
            embed.add_field(
                name="Error", value="Invalid number of arguments.", inline=False
            )
            embed.set_footer(text="FP Sneakers | " + version)

            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="FP Sneakers Discord Invite", color=0xA5F2F3)
            embed.set_thumbnail(url="https://i.imgur.com/O5HEApC.png")
            embed.add_field(name="Discord Invite Link:", value=discordinv)
            embed.set_footer(text="FP Sneakers | " + version)

            await message.channel.send(embed=embed)

    if message.content.split()[0] == prefix + "commands":
        if len(message.content.split(" ")) != 1:
            embed = discord.Embed(title="FP Sneakers Discord Bot Commands")
            embed.add_field(
                name="Error", value="Invalid number of arguments.", inline=False
            )
            embed.set_footer(text="FP Sneakers | " + version)

            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="FP Sneakers Discord Bot Commands", color=0xA5F2F3
            )
            embed.set_thumbnail(url="https://i.imgur.com/O5HEApC.png")
            for command in COMMANDS:
                embed.add_field(
                    name=command["name"], value=command["description"], inline=False
                )
            embed.set_footer(text="FP Sneakers | " + version)

            await message.channel.send(message.author, embed=embed)

    if message.content.split()[0] == prefix + "help":
        if len(message.content.split(" ")) != 1:
            embed = discord.Embed(title="FP Sneakers Discord Bot")
            embed.add_field(
                name="Error", value="Invalid number of arguments.", inline=False
            )
            embed.set_footer(text="FP Sneakers | " + version)

            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="", url=fpsite, color=0xA5F2F3)
            embed.set_author(name="FP Sneakers Discord Bot")
            embed.set_thumbnail(url="https://i.imgur.com/O5HEApC.png")
            embed.add_field(
                name="Default Prefix",
                value="The prefix set for the bot is '**{}**'\nCommands are case sensitive.".format(
                    prefix
                ),
                inline=False,
            )
            embed.add_field(
                name="Commands",
                value="?ping\n?stockx\n?stockxfees\n?goat\n?atc\n?shopifycheck\n?supnycost\n?supweek\n?addy\n?inv\n?commands - *Gives information on proper command usage and a description on what each command does*\n",
                inline=False,
            )
            embed.add_field(
                name="Discord bot built for FP Sneakers",
                value="By <@147208559925395456> <@148567967435587584> <@183828504847056897>",
                inline=False,
            )
            embed.set_footer(text="FP Sneakers | " + version)

            await message.channel.send(message.author, embed=embed)


@client.event
async def on_ready():

    print("FP SNEAKERS BOT LAUNCHED")
    print("Version: " + version)
    await client.change_presence(
        status=discord.Game(name="FPSNKRS | " + prefix + "help")
    )


client.run(token)
