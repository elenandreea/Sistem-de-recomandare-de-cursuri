import { Component, OnInit } from '@angular/core';
import { Course } from '../course'

import { BackendConnectionService } from '../backend-connection.service';
import { filter } from 'rxjs/operators';

@Component({
  selector: 'app-courses-list',
  templateUrl: './courses-list.component.html',
  styleUrls: ['./courses-list.component.css']
})
export class CoursesListComponent implements OnInit {
  courses : Course[];
  isTop: Boolean = true;

  constructor(private courseService: BackendConnectionService) { }

  ngOnInit(): void {
    this.getCourses();
  }

  getCourses(): void {
    this.courseService.getCourses()
    .subscribe(courses => this.courses = courses)
  }

  getFilters(): void{
    var filters = [];
    var count;


    //Search
    var search = document.getElementsByClassName("input_search");
    var search_arr = []
    if(search[0].value != "" || search[0].value != undefined) {
      // filters['search'] = search.value;
      search_arr.push(search[0].value)
    }
    filters.push({"search":search_arr})

    // Websites
    var websites = document.getElementsByClassName("checkbox_website");
    filters['website'] = [];
    var website_arr = []
    for(var i=0; i<websites.length; i++) {
      if(websites[i].checked == true) {
        website_arr.push(websites[i].value);
      }
    }
    filters.push({"website":website_arr})

    // Difficulty
    var difficulties = document.getElementsByClassName("checkbox_difficulty");
    filters['difficulty'] = [];
    var difficulty_arr = []
    for(var i=0; i<difficulties.length; i++) {
      if(difficulties[i].checked == true) {
        difficulty_arr.push(difficulties[i].value);
      }
    }
    filters.push({"difficulty":difficulty_arr})

    // Ratings
    var ratings = document.getElementsByClassName("checkbox_ratings");
    filters['rating'] = [];
    var rating_arr = [];
    for(var i=0; i<ratings.length; i++) {
      if(ratings[i].checked == true) {
        rating_arr.push(ratings[i].value);
      }
    }
    filters.push({"rating":rating_arr})

    // Tags
    var tags = document.getElementsByClassName("checkbox_categories");
    filters['tags'] = [];
    var tags_arr = [];
    for(var i=0; i<tags.length; i++) {
      if(tags[i].checked == true) {
        tags_arr.push(tags[i].value);
      }
    }
    filters.push({"tags":tags_arr})
    console.log(filters)

    this.courseService.getCoursesWithFilters(filters)
    .subscribe(courses => this.courses = courses)

    this.isTop = false;
  }
}
