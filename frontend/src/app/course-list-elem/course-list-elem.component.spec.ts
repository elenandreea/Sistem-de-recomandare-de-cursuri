import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CourseListElemComponent } from './course-list-elem.component';

describe('CourseListElemComponent', () => {
  let component: CourseListElemComponent;
  let fixture: ComponentFixture<CourseListElemComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CourseListElemComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CourseListElemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
