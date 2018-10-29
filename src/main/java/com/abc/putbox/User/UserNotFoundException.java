package com.abc.putbox.User;

public class UserNotFoundException extends Exception {

    public UserNotFoundException(){
        super();
    }

    public UserNotFoundException(String mes) {
        super(mes);
    }
}
