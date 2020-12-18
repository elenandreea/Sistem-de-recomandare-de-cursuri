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
  recommandUsers: Course[]

  constructor(private route: ActivatedRoute,private courseService: BackendConnectionService) {
   }

  ngOnInit(): void {
    var id = this.route.snapshot.paramMap.get('courseId');
    console.log(id);
    if(id) {
      this.getCourse(id);
      // this.getSimilarCourses(id);
    }
    
  }

  getCourse(id : String): void {
    this.courseService.getCourse(id)
    .subscribe((course: Course) => {
      this.course = course;
      this.getRecommandUsers(this.course.name);
    });
  }

  getSimilarCourses(id : String): void {
    this.courseService.getSimilarCourses(id)
    .subscribe(courses => this.similarCourses = courses)
  }

  getRecommandUsers(name: String): void {
    console.log("AICI")
    this.courseService.getRecommandUsers(name)
    .subscribe(courses => this.recommandUsers = courses)
  }
}
