import { Component, OnInit } from '@angular/core';
import { Input } from '@angular/core';
import { Course } from '../course';

@Component({
  selector: 'app-recommended-course',
  templateUrl: './recommended-course.component.html',
  styleUrls: ['./recommended-course.component.css']
})
export class RecommendedCourseComponent implements OnInit {

  @Input('course') course: Course;
  
  showUdemy: boolean;
  route: string;

  constructor() {}
  
  ngOnInit(): void {
    if(this.course.website == "Udemy") {
      this.showUdemy = true;
    }
    this.route= "/course/"+this.course.id;
  }

}
