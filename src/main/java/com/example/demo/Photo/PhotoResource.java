package com.example.demo.Photo;

import java.net.URI;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

@RestController
public class PhotoResource {

    @Autowired
    private PhotoRepository PhotoRepository;

    @GetMapping("/Photos")
    public List<Photo> retrieveAllPhotos() {
        return PhotoRepository.findAll();
    }

    @GetMapping("/Photos/{id}")
    public Photo retrievePhoto(@PathVariable long id) {
        Optional<Photo> Photo = PhotoRepository.findById(id);

        if (!Photo.isPresent())
            try {
                throw new PhotoNotFoundException("id-" + id);
            } catch (Exception e) {
                e.printStackTrace();
            }
        return Photo.get();
    }

    @DeleteMapping("/Photos/{id}")
    public void deletePhoto(@PathVariable long id) {
        PhotoRepository.deleteById(id);
    }

    @PostMapping("/Photos")
    public ResponseEntity<Object> createPhoto(@RequestBody Photo Photo) {
        Photo savedPhoto = PhotoRepository.save(Photo);

        URI location = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}")
                .buildAndExpand(savedPhoto.getPhoto_id()).toUri();

        return ResponseEntity.created(location).build();

    }

    @PutMapping("/Photos/{id}")
    public ResponseEntity<Object> updatePhoto(@RequestBody Photo Photo, @PathVariable long id) {

        Optional<Photo> PhotoOptional = PhotoRepository.findById(id);

        if (!PhotoOptional.isPresent())
            return ResponseEntity.notFound().build();

        Photo.setPhoto_id(id);

        PhotoRepository.save(Photo);

        return ResponseEntity.noContent().build();
    }
}
