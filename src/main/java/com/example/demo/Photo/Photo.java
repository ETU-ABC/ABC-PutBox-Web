package com.example.demo.Photo;


import com.example.demo.User.User;
import javax.persistence.*;
import java.util.Set;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

@Entity
public class Photo {
    @Id
    @GeneratedValue
    private Long photo_id;
    private String image;
    private String upload_date;
    private String upload_by;


    public Photo() {
        super();
    }

    public Photo(Long photo_id, String image, String upload_date,String upload_by) {
        super();
        this.photo_id = photo_id;
        this.image = image;
        this.upload_date = upload_date;
        this.upload_by=upload_by;

    }


    public Long getPhoto_id() {
        return photo_id;
    }

    public void setPhoto_id(Long photo_id) {
        this.photo_id = photo_id;
    }

    public String getImage() {
        return image;
    }

    public void setImage(String image) {
        this.image = image;
    }

    public String getUpload_date() {
        return upload_date;
    }

    public void setUpload_date(String upload_date) {
        this.upload_date = upload_date;
    }

    public String getUpload_by() {
        return upload_by;
    }

    public void setUpload_by(String upload_by) {
        this.upload_by = upload_by;
    }


}