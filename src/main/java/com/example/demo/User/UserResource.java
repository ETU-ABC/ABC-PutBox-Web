package com.example.demo.User;

import com.example.demo.User.User;
import com.example.demo.User.UserNotFoundException;
import com.example.demo.User.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.net.URI;
import java.util.List;
import java.util.Optional;

@RestController
public class UserResource {

    @Autowired
    private UserRepository UserRepository;

    @GetMapping("/Users")
    public List<User> retrieveAllUsers() {
        return UserRepository.findAll();
    }

    @GetMapping("/Users/{id}")
    public User retrieveUser(@PathVariable long id) {
        Optional<User> User = UserRepository.findById(id);

        if (!User.isPresent())
            try {
                throw new UserNotFoundException("id-" + id);
            } catch (Exception e) {
                e.printStackTrace();
            }
        return User.get();
    }

    @DeleteMapping("/Users/{id}")
    public void deleteUser(@PathVariable long id) {
        UserRepository.deleteById(id);
    }

    @PostMapping("/Users")
    public ResponseEntity<Object> createUser(@RequestBody User User) {
        User savedUser = UserRepository.save(User);

        URI location = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}")
                .buildAndExpand(savedUser.getUser_id()).toUri();

        return ResponseEntity.created(location).build();

    }

    @PutMapping("/Users/{id}")
    public ResponseEntity<Object> updateUser(@RequestBody User User, @PathVariable long id) {

        Optional<User> UserOptional = UserRepository.findById(id);

        if (!UserOptional.isPresent())
            return ResponseEntity.notFound().build();

        User.setUser_id(id);

        UserRepository.save(User);

        return ResponseEntity.noContent().build();
    }
}
