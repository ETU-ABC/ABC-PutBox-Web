package com.abc.putbox.Student;

public class StudentNotFoundException extends Exception {

    public StudentNotFoundException(){
        super();
    }

    public StudentNotFoundException(String mes) {
        super(mes);
    }
}
