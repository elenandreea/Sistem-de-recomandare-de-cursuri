import { Component, OnInit } from '@angular/core';
import { Course } from '../course';

import { Router, ActivatedRoute, ParamMap } from '@angular/router';

import { BackendConnectionService } from '../backend-connection.service';

@Component({
  selector: 'app-single-course',
  templateUrl: './single-course.component.html',
  styleUrls: ['./single-course.component.css']
})
export class SingleCourseComponent implements OnInit {

  course: Course
  isUdemy: boolean
  courseId: number
  similarCourses: Course[]

  constructor(private route: ActivatedRoute,private courseService: BackendConnectionService) {
    // this.course = {
    //   id: 1,
    //   name: "Ultimate Investment Banking Course",
    //   url: "https://www.udemy.com/ultimate-investment-banking-course/",
    //   rating: 3.9,
    //   difficulty: "All Levels",
    //   tags: "Business Finance",
    //   website: "Udemy",
    //   description: 'descriere descriere descriere descriere descriere descriere descriere descriere descriere descriere descriere descriere descriere descriere'
    // };
    // this.isUdemy = this.course.website == "Udemy" ? true : false
   }

  ngOnInit(): void {
    var id = this.route.snapshot.paramMap.get('courseId');
    console.log(id);
    this.getCourse(id);
    this.getSimilarCourses(id);
  }

  getCourse(id : String): void {
    this.courseService.getCourse(id)
    .subscribe(course => this.course = course)
  }

  getSimilarCourses(id : String): void {
    this.courseService.getSimilarCourses(id)
    .subscribe(courses => this.similarCourses = courses)
  }
}
