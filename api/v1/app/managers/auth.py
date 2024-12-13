#!/usr/bin/python3

from decouple import config
from fastapi import HTTPException, status

from ....supabase.supabase_client import supabase
from ..schemas.resquests.user import UpdateUser, SignInUser
from ..schemas.responses.custom_responses import UNEXPECTED_ERROR

EMAIL_SIGN_UP_REDIRECT_URL = f"{config('SITE_HOST'), config('SITE_PORT')}"


class AuthManager:
    @staticmethod
    async def create_user(user_data):
        """Registers a user and returns the response or error."""
        try:
            await supabase.auth.sign_up(
                {
                    "email": "email@example.com",
                    "password": "password",
                    "options": {"data": f"{(UpdateUser(**user_data))}"}
                }
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e)
        # I am putting this here incase we need to redirect our users to a special page after they are just registered.
        # 'options': {
        #     'email_redirect_to': EMAIL_SIGN_UP_REDIRECT_URL,
        # }

    @staticmethod
    async def update_user(data_to_update):
        """
        This function handles user profile update
        :param data_to_update:
        :return: A user object as user profile
        """
        try:
            response = await supabase.auth.update_user({
                "data": UpdateUser(**data_to_update)
            })
            return response
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{e}")

    @staticmethod
    async def sign_in_user_with_passwd_and_email(user_data):
        """
        This function sings in a user provided the user has the correct credentials, such as email and password
        :param user_data: the user's details
        :return: it signs in a user if the credentials are correct.
        """
        try:
            await supabase.auth.sign_in_with_password(
                SignInUser(**user_data)
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{e}")


    @staticmethod
    async def sign_in_with_email_otp(email):
        """
        This will help sign in user with their registered email.
        :param email:
        :return:
        """
        response = await supabase.auth.sign_in_with_otp(
            {
                "email": email,
                "options": {"email_redirect_to": EMAIL_SIGN_UP_REDIRECT_URL},
            }
        )
        return response

    @staticmethod
    async def sign_in_with_sms_otp(phone_number):
        """
        This will sign in user with their phone number.
        :param phone_number:
        :return:
        """
        response = await supabase.auth.sign_in_with_otp({
            "phone": phone_number,
        })
        return response

    @staticmethod
    async def sign_in_user_with_whatsapp(whatsapp_number):
        """
        This will sign in user with their WhatsApp number.
        :param whatsapp_number:
        :return:
        """
        response = await supabase.auth.sign_in_with_otp({
            "phone": whatsapp_number,
            "options": {
                "channel": "whatsapp",
            }
        })
        return response

    @staticmethod
    async def sign_in_user_with_third_party(third_party_name):
        """
        This will sign in user with third-party app such as Google, Facebook etc.
        :param third_party_name:
        :return:
        """
        response = await supabase.auth.sign_in_with_oauth({
            "provider": third_party_name
        })
        return response

    @staticmethod
    async def sign_out_user():
        """
        This function will sign out user from the app
        :return:
        """
        response = await supabase.auth.sign_out()

        return response

    @staticmethod
    async def reset_password(email):
        """
        This will take a user's email and sends a link to the email for the user to reset their password.
        :param email:
        :return:
        """
        await supabase.auth.reset_password_for_email(email, {
            "redirect_to": "https://example.com/update-password",
        })

    @staticmethod
    async def confirm_update_password(new_password):
        """
        This will make the user input their desired new password.
        :param new_password:
        :return:
        """
        response = supabase.auth.update_user({
            "password": new_password
        })
        return response

