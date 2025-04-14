import streamlit_authenticator as stauth

# Reemplaza con tu contraseña real
passwords = ['demo123']

hashed_passwords = stauth.Hasher(passwords).generate()
print(hashed_passwords)
