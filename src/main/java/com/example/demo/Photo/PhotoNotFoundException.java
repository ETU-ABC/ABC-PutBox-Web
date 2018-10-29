package com.example.demo.Photo;

public class PhotoNotFoundException extends Exception {

    public PhotoNotFoundException(){
        super();
    }

    public PhotoNotFoundException(String mes) {
        super(mes);
    }
}
