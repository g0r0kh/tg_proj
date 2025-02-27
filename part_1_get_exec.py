import requests
import pandas as pd
import os
import schedule
import asyncio
## telegram libs
from telegram import Bot, Update
from datetime import date, datetime, timedelta
# qr libs
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer



class TBot:
    def __init__(self, bot_token, chat_id):
        self.bot = Bot(bot_token)
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"


    async def posting_group(self):
        # Add file with posts send dates and pictures path
        #df_schedule = pd.read_csv(os.path.expanduser('~/Desktop/tg_repo/text_schedule.txt'), sep='\t')  # read txt file
        try:
            df_schedule = pd.read_csv(os.path.join(os.path.dirname(__file__), 'tg_repo (copy)', 'text_schedule.txt'), sep='\t')
            df_schedule['dt_time'] = pd.to_datetime(df_schedule['dt_time'])  # transform to datetype
            curr_date_posts = df_schedule[(df_schedule['dt_time'] > pd.Timestamp.now()) &
                                          (df_schedule['dt_time'].dt.date == pd.Timestamp.now().normalize().date())]
            if not curr_date_posts.empty:
                for index in range(len(curr_date_posts)):
                    schedule_time = str(curr_date_posts.iloc[index, 0].time())[:-3]
                    schedule.every().day.at(schedule_time)


                    while True:
                        schedule.run_pending()

                        message = "\n".join(curr_date_posts.iloc[index, 1].strip()).replace('\n', ' ').replace('\r', '')
                        await self.bot.send_photo(chat_id=self.chat_id, caption=message,
                                        photo=open(os.path.expanduser(curr_date_posts.iloc[index, 2].strip()), 'rb'))
                        index+=1
                        await asyncio.sleep(43)

        except (FileNotFoundError, ValueError, requests.exceptions.RequestException) as e:
            print(f"Error in posting_group: {e}")

    async def generate_invite_link(self):
        #link_name
        # df_schedule = pd.read_csv(os.path.join(os.path.dirname(__file__), 'tg_repo', 'text_schedule.txt'), sep='\t')
        try:
            df_main = pd.read_csv(os.path.join(os.path.dirname(__file__), 'tg_repo (copy)', 'invite_data.txt'), sep='\t')

            # fill gaps in links file.txt
            for index, row in df_main.iterrows():
                if pd.isnull(row['id_link']):
                    link_name = row['id']

                    expire_date = (datetime.combine(date.today() + timedelta(days=3), datetime.min.time()) - datetime.strptime('1970-01-01', '%Y-%m-%d')).total_seconds()
                    creates_join_request = True
                    is_primary = True
                    is_revoked = True


                    response = requests.post(f"{self.base_url}/createChatInviteLink",
                                             json={
                                                 "chat_id": self.chat_id,
                                                 "name": link_name,
                                                 "creates_join_request": creates_join_request,
                                                 "is_primary": is_primary,
                                                 "is_revoked": is_revoked,
                                                 "expire_date": expire_date
                                             })
                    response.raise_for_status()
                    invite = response.json()

                    df_main.at[index, 'id_link'] = invite["result"]["name"]
                    df_main.at[index, 'link'] = invite["result"]["invite_link"]
                    df_main.at[index, 'dt_create'] = date.today()
                    df_main.at[index, 'dt_expire'] = invite["result"]["expire_date"]

            # keep result in links.txt
            #         df_main = pd.read_csv(os.path.join(os.path.dirname(__file__), 'tg_repo', 'invite_data.txt'), sep='\t')
                    df_main.to_csv(os.path.join(os.path.dirname(__file__), 'tg_repo (copy)', 'invite_data.txt'), sep='\t', index=False)
            # QR linked
                    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
                    qr.add_data(invite["result"]["invite_link"])

            #QR image produce
                    img = qr.make_image(image_factory=StyledPilImage, module_drawer=CircleModuleDrawer())

            # keep QR
            #         qr_path = os.path.join(os.path.expanduser("~"), "Desktop/tg_repo/links")
            #         file_path = os.path.join(qr_path, f"{link_name}.png")
                    current_dir = os.path.dirname(__file__)
                    qr_path = os.path.join(current_dir, 'tg_repo (copy)', 'links')
                    file_path = os.path.join(qr_path, f"{link_name}.png")

            # save QR
                    img.save(file_path)

        except (FileNotFoundError, ValueError, requests.exceptions.RequestException) as e:
                    print(f"Error in generate_invite_link: {e}")
async def main():
    try:
        # set up TOKEN & CHAT ID
        df = pd.read_csv('~/Desktop/key_b.txt', header=None) # HIDE WHEN 102 & 103 FILLED PROPPER
        bot_token = df.iloc[0, 0] # move df.iloc[0, 0] and ADD HERE 'YOUR_BOT_TOKEN' instead
        chat_id = df.iloc[1, 0]   # move df.iloc[1, 0] and ADD HERE 'YOUR_CHAT_ID' or '..GROUP..' instead

        # BOT exec
        bot = TBot(bot_token, chat_id)

        # # main circle
        await asyncio.gather(bot.posting_group()
                             , bot.generate_invite_link()
                         , )
    except (FileNotFoundError, ValueError, requests.exceptions.RequestException) as e:
            print(f"Error in main: {e}")

if __name__ == "__main__":
    asyncio.run(main())